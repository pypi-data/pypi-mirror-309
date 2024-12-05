import asyncio
import inspect
import json
import time
from functools import wraps
from textwrap import dedent
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

import litellm
from loguru import logger
from pydantic import BaseModel
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from neat.config import STRUCTURED_OUTPUT_MODELS, UNSUPPORTED_TOOL_MODELS, settings
from neat.constants import LLMModel
from neat.database import init_db, load_prompt, save_execution, save_prompt
from neat.exceptions import (
    IncompatibleArgumentsError,
    TemperatureRangeError,
    UnsupportedModelFeaturesError,
)
from neat.models import ExecutionData, Message, PromptData, UsageStats
from neat.tools import ToolManager
from neat.utils import extract_code_block, generate_output_schema, hash

litellm.suppress_debug_info = True
litellm.set_verbose = False
litellm.telemetry = False
litellm.drop_params = True
litellm.add_function_to_prompt = True
console = Console()

T = TypeVar("T", bound=BaseModel)
StreamContent = Union[str, T, Dict[str, Any]]
ComboMessage = Union[Message, Dict[str, str]]  # New type alias


class Neat:
    def __init__(self):
        self.tool_manager: ToolManager = ToolManager()
        self.usage: UsageStats = UsageStats()

    def _validate_inputs(
        self,
        model: Union[LLMModel, str],
        temp: float,
        tools: List[Callable],
        response_model: Optional[Type[T]],
    ) -> str:
        if isinstance(model, LLMModel):
            model = model.model_name
        elif isinstance(model, str):
            model = model
        if not isinstance(temp, (int, float)) or temp < 0 or temp > 1:
            raise TemperatureRangeError("Temperature must be a float between 0 and 1")

        if model in UNSUPPORTED_TOOL_MODELS and (tools or response_model):
            raise UnsupportedModelFeaturesError(
                f"Tool calling or structured outputs are not supported for the {model} model."
            )

        if tools and response_model:
            raise IncompatibleArgumentsError(
                "Cannot set both 'tools' and 'response_model'. Please choose one or the other."
            )
        return model

    def _get_environment_representation(self, func: Callable) -> Dict[str, Dict[str, Any]]:
        closure = inspect.getclosurevars(func)
        return {
            "nonlocals": {k: v for k, v in closure.nonlocals.items() if not k.startswith("__")},
            "globals": {
                k: v for k, v in closure.globals.items() if not k.startswith("__") and k != "ell"
            },
        }

    def _handle_database_operations(
        self,
        func: Callable,
        func_name: str,
        model: str,
        temperature: float,
        messages: List[Message],
    ) -> Tuple[Optional[int], Optional[PromptData], List[Message]]:
        init_db()
        env_repr = self._get_environment_representation(func)
        func_hash = hash(inspect.getsource(func))
        env_hash = hash(json.dumps(env_repr, sort_keys=True))
        version_hash = hash(func_hash + env_hash)

        existing_prompt = load_prompt(func_name)

        if existing_prompt and existing_prompt.hash == version_hash:
            logger.debug(
                f"Using existing prompt version for '{func_name}': v{existing_prompt.version}"
            )
            return (
                existing_prompt.id,
                existing_prompt,
                [Message(**m) for m in json.loads(existing_prompt.prompt)],
            )

        new_version = (existing_prompt.version + 1) if existing_prompt else 1
        prompt_content = json.dumps(
            [m.model_dump(exclude_none=True, exclude_unset=True) for m in messages]
        )

        prompt_data = PromptData(
            func_name=func_name,
            version=new_version,
            hash=version_hash,
            model=model,
            temperature=temperature,
            prompt=prompt_content,
            environment=json.dumps(env_repr, default=str),
        )
        prompt_id = save_prompt(prompt_data)
        logger.debug(f"New prompt version created for '{func_name}': v{new_version}")

        return prompt_id, prompt_data, messages

    def _generate_api_params(
        self,
        model: str,
        messages: Sequence[Message],
        temperature: float,
        response_model: Optional[Type[T]],
        tool_definitions: List[Dict[str, Any]],
        stream: bool = False,
    ) -> Dict[str, Any]:
        api_params: Dict[str, Any] = {
            "model": model,
            "messages": [m.model_dump(exclude_none=True, exclude_unset=True) for m in messages],
            "temperature": temperature,
            # "max_tokens": 4000,
            "stream": stream,
        }

        if response_model:
            if model in STRUCTURED_OUTPUT_MODELS:
                api_params["response_format"] = response_model
            else:
                api_params["tools"] = [
                    {
                        "type": "function",
                        "function": generate_output_schema(response_model),
                    }
                ]
                api_params["tool_choice"] = "auto"
                api_params["messages"].append(
                    {
                        "role": "user",
                        "content": f"Call the {response_model.__name__} function to answer the question above.",
                    }
                )
        elif tool_definitions:
            api_params["tools"] = tool_definitions
            api_params["tool_choice"] = "auto"

        return api_params

    async def _interact_with_llm_stream(
        self,
        messages: Sequence[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[T]],
    ) -> AsyncGenerator[StreamContent, None]:
        api_params = self._generate_api_params(
            model, messages, temperature, response_model, tool_definitions, stream=True
        )

        accumulated_content = ""
        accumulated_function_args = ""
        current_function_name = None

        async for chunk in await litellm.acompletion(**api_params):  # type: ignore
            delta = chunk.choices[0].delta

            # Handle usage data if present
            if hasattr(chunk, "usage") and chunk.usage:
                # Calculate costs and update usage stats
                prompt_cost, completion_cost = litellm.cost_calculator.cost_per_token(
                    model=model,
                    prompt_tokens=chunk.usage.prompt_tokens,
                    completion_tokens=chunk.usage.completion_tokens,
                )
                total_cost = (prompt_cost or 0) + (completion_cost or 0)
                self.usage.update(
                    model=model,
                    prompt_tokens=chunk.usage.prompt_tokens,
                    completion_tokens=chunk.usage.completion_tokens,
                    cost=total_cost,
                )
                continue

            if delta.content is not None:
                accumulated_content += delta.content
                yield delta.content

            if delta.tool_calls:
                for tool_call in delta.tool_calls:
                    if tool_call.function.name and not current_function_name:
                        current_function_name = tool_call.function.name
                    if tool_call.function.arguments:
                        accumulated_function_args += tool_call.function.arguments

                    if accumulated_function_args:
                        try:
                            parsed_args = json.loads(accumulated_function_args)
                            if response_model:
                                validated_content = response_model.model_validate(parsed_args)
                                yield validated_content
                            else:
                                yield {"function": current_function_name, "arguments": parsed_args}
                        except json.JSONDecodeError:
                            continue

    async def _interact_with_llm_sync(
        self,
        messages: Sequence[Message],
        model: str,
        temperature: float,
        tool_definitions: List[Dict[str, Any]],
        response_model: Optional[Type[T]],
    ) -> Tuple[Any, Union[str, T]]:
        api_params = self._generate_api_params(
            model, messages, temperature, response_model, tool_definitions
        )
        llm_response = await litellm.acompletion(**api_params)
        llm_message = llm_response.choices[0].message  # type: ignore

        # Calculate cost and update usage stats
        prompt_cost, completion_cost = litellm.cost_calculator.cost_per_token(
            model=model,
            prompt_tokens=llm_response.usage.prompt_tokens,  # type: ignore
            completion_tokens=llm_response.usage.completion_tokens,  # type: ignore
        )
        total_cost = (prompt_cost or 0) + (completion_cost or 0)
        self.usage.update(
            model=model,
            prompt_tokens=llm_response.usage.prompt_tokens,  # type: ignore
            completion_tokens=llm_response.usage.completion_tokens,  # type: ignore
            cost=total_cost,
        )

        if not llm_message.content:
            llm_message.content = ""  # Patch for litellm+cohere compatibility

        if response_model:
            try:
                if llm_message.tool_calls:
                    tool_call_arguments = llm_message.tool_calls[0].function.arguments
                    parsed_content = (
                        json.loads(tool_call_arguments)
                        if isinstance(tool_call_arguments, str)
                        else tool_call_arguments
                    )
                else:
                    parsed_content = json.loads(extract_code_block(llm_message.content))

                validated_content = response_model.model_validate(parsed_content)
                return llm_response, validated_content

            except json.JSONDecodeError as e:
                logger.error(f"Error parsing response: {e}")
                raise

        return llm_response, llm_message.content

    async def process_messages_stream(
        self,
        messages: Sequence[Union[Message, Dict[str, str]]],  # Accept both types
        model: str,
        temperature: float,
        tools: List[Callable],
        response_model: Optional[Type[T]],
        use_db: bool,
        max_iterations: int,
    ) -> AsyncGenerator[StreamContent, None]:
        # Convert messages to Message objects if needed
        processed_messages: List[Message] = [
            Message.from_dict(m) if isinstance(m, dict) else m for m in messages
        ]

        tool_definitions = (
            self.tool_manager.get_tool_definitions() if tools and not response_model else []
        )

        async for chunk in self._interact_with_llm_stream(
            processed_messages,
            model,
            temperature,
            tool_definitions,
            response_model,
        ):
            yield chunk

    async def process_messages_sync(
        self,
        messages: Sequence[ComboMessage],
        model: str,
        temperature: float,
        tools: List[Callable],
        response_model: Optional[Type[T]],
        use_db: bool,
        max_iterations: int,
        conversation: bool,
        prompt_id: Optional[int],
    ) -> Union[T, str]:
        # Convert messages to Message objects if needed
        processed_messages: List[Message] = [
            Message.from_dict(m) if isinstance(m, dict) else m for m in messages
        ]

        tool_definitions = (
            self.tool_manager.get_tool_definitions() if tools and not response_model else []
        )

        start_time = time.time()
        message_content: Optional[Union[str, T]] = None

        while True:
            for iteration in range(max_iterations):
                llm_response, content = await self._interact_with_llm_sync(
                    processed_messages,
                    model,
                    temperature,
                    tool_definitions,
                    response_model,
                )

                llm_message = llm_response.choices[0].message
                if not llm_message:
                    raise ValueError("No message returned from LLM")

                processed_messages.append(Message(**llm_message.model_dump(exclude_none=False)))

                if response_model:
                    message_content = content
                    break

                if not llm_message.tool_calls:
                    message_content = content
                    break

                for tool_call in llm_message.tool_calls:
                    function_name = str(tool_call.function.name)
                    function_args = json.loads(tool_call.function.arguments)
                    logger.debug(f"Calling tool: {function_name}")

                    function_response = await self.tool_manager.use_tool(
                        function_name, function_args
                    )
                    logger.debug(f"function response: {function_response}")

                    processed_messages.append(
                        Message(
                            tool_call_id=tool_call.id,
                            role="tool",
                            name=function_name,
                            content=str(function_response),
                        )
                    )
            else:
                logger.warning(
                    f"Reached maximum iterations ({max_iterations}) without resolution"
                )
                break

            if conversation:
                console.print(
                    Panel(
                        Markdown(str(message_content) or ""),
                        title="AI",
                        border_style="cyan",
                    )
                )
                user_input = console.input("[bold green]You:[/bold green] ")

                if user_input.lower() in ["exit", "quit"]:
                    console.print("[bold red]Exiting conversation...[/bold red]")
                    break
                if user_input == "":
                    user_input = " "
                processed_messages.append(Message(role="user", content=user_input))
                continue
            else:
                break

        if use_db and prompt_id is not None:
            execution_time = time.time() - start_time
            execution_data = ExecutionData(
                version_id=prompt_id,
                prompt_tokens=self.usage.total_prompt_tokens,
                completion_tokens=self.usage.total_completion_tokens,
                execution_time=execution_time,
            )
            await asyncio.to_thread(save_execution, execution_data)

        if message_content is None:
            raise ValueError("No content generated from LLM interaction")

        return message_content


    @overload
    def lm(
        self,
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: Type[T],
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[False] = False,
    ) -> Callable[
        [Callable[..., Awaitable[Sequence[ComboMessage]]]], Callable[..., Awaitable[T]]
    ]: ...

    @overload
    def lm(
        self,
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: Type[T],
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[True],
    ) -> Callable[
        [Callable[..., Awaitable[Sequence[ComboMessage]]]],
        Callable[..., Awaitable[AsyncGenerator[Union[str, T], None]]],
    ]: ...

    @overload
    def lm(
        self,
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: None = None,
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[False] = False,
    ) -> Callable[
        [Callable[..., Awaitable[Sequence[ComboMessage]]]], Callable[..., Awaitable[str]]
    ]: ...

    @overload
    def lm(
        self,
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: None = None,
        use_db: bool = ...,
        conversation: bool = ...,
        stream: Literal[True],
    ) -> Callable[
        [Callable[..., Awaitable[Sequence[ComboMessage]]]],
        Callable[..., Awaitable[AsyncGenerator[StreamContent, None]]],
    ]: ...

    def lm(
        self,
        *,
        model: Union[LLMModel, str] = settings.default_model,
        temperature: float = settings.default_temperature,
        tools: List[Callable] = [],
        response_model: Optional[Type[T]] = None,
        use_db: bool = False,
        max_iterations: int = 20,
        conversation: bool = False,
        stream: bool = False,
    ) -> Callable[
        [Callable[..., Awaitable[Sequence[ComboMessage]]]],
        Callable[..., Awaitable[Union[T, str, AsyncGenerator[StreamContent, None]]]],
    ]:
        """
        Async decorator for language model interactions.

        Args:
            model: The language model to use
            temperature: Sampling temperature
            tools: Optional list of tool functions to use
            response_model: Optional Pydantic model for structured output
            use_db: Whether to use database logging
            max_iterations: Maximum number of tool call iterations
            conversation: Whether to enable conversation mode
            stream: Whether to stream the response

        Returns:
            A decorated function that returns either:
            - A single response (when stream=False)
            - An async generator yielding response chunks (when stream=True)
        """
        model = self._validate_inputs(model, temperature, tools, response_model)

        def decorator(
            func: Callable[..., Awaitable[Sequence[ComboMessage]]],
        ) -> Callable[..., Awaitable[Union[T, str, AsyncGenerator[StreamContent, None]]]]:
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("The decorated function must be async. Use 'async def'.")

            @wraps(func)
            async def wrapper(
                *args: Any, **kwargs: Any
            ) -> Union[T, str, AsyncGenerator[StreamContent, None]]:
                messages = await func(*args, **kwargs)

                prompt_id = None
                if use_db and not stream:  # Database operations only for non-streaming mode
                    processed_messages = [
                        Message.from_dict(m) if isinstance(m, dict) else m for m in messages
                    ]
                    prompt_id, _, processed_messages = await asyncio.to_thread(
                        self._handle_database_operations,
                        func,
                        func.__name__,
                        model,
                        temperature,
                        processed_messages,
                    )
                    messages = processed_messages  # Use the processed messages from DB

                if stream:
                    # Return an async generator wrapped in a coroutine
                    async def generator_wrapper():
                        async for chunk in self.process_messages_stream(
                            messages,
                            model,
                            temperature,
                            tools,
                            response_model,
                            use_db,
                            max_iterations,
                        ):
                            yield chunk

                    return generator_wrapper()
                else:
                    return await self.process_messages_sync(
                        messages,
                        model,
                        temperature,
                        tools,
                        response_model,
                        use_db,
                        max_iterations,
                        conversation,
                        prompt_id,
                    )

            return wrapper

        return decorator

    # Overloads for lm_run method
    @overload
    def lm_run(
        self,
        messages: Sequence[ComboMessage],
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: Type[T],
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[False] = False,
    ) -> Coroutine[Any, Any, T]: ...

    @overload
    def lm_run(
        self,
        messages: Sequence[ComboMessage],
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: Type[T],
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[True],
    ) -> Coroutine[Any, Any, AsyncGenerator[Union[str, T], None]]: ...

    @overload
    def lm_run(
        self,
        messages: Sequence[ComboMessage],
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: None = None,
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[False] = False,
    ) -> Coroutine[Any, Any, str]: ...

    @overload
    def lm_run(
        self,
        messages: Sequence[ComboMessage],
        *,
        model: Union[LLMModel, str] = ...,
        temperature: float = ...,
        tools: List[Callable] = ...,
        response_model: None = None,
        use_db: bool = ...,
        max_iterations: int = ...,
        conversation: bool = ...,
        stream: Literal[True],
    ) -> Coroutine[Any, Any, AsyncGenerator[StreamContent, None]]: ...

    # Main lm_run method
    def lm_run(
        self,
        messages: Sequence[ComboMessage],
        *,
        model: Union[LLMModel, str] = settings.default_model,
        temperature: float = settings.default_temperature,
        tools: List[Callable] = [],
        response_model: Optional[Type[T]] = None,
        use_db: bool = False,
        max_iterations: int = 20,
        conversation: bool = False,
        stream: bool = False,
    ) -> Coroutine[Any, Any, Union[T, str, AsyncGenerator[StreamContent, None]]]:
        """
        Direct method for language model interactions without using a decorator.

        Args:
            messages: A sequence of Message or dicts representing the conversation.
            model: The language model to use.
            temperature: Sampling temperature.
            tools: Optional list of tool functions to use.
            response_model: Optional Pydantic model for structured output.
            use_db: Whether to use database logging.
            max_iterations: Maximum number of tool call iterations.
            conversation: Whether to enable conversation mode.
            stream: Whether to stream the response.

        Returns:
            A coroutine that returns either:
            - A single response (when stream=False)
            - An async generator yielding response chunks (when stream=True)
        """
        model = self._validate_inputs(model, temperature, tools, response_model)

        async def _lm_run_impl() -> Union[T, str, AsyncGenerator[StreamContent, None]]:
            prompt_id = None
            if use_db and not stream:  # Database operations only for non-streaming mode
                # We need a dummy function for environment representation
                dummy_func = lambda: None
                processed_messages = [
                    Message.from_dict(m) if isinstance(m, dict) else m for m in messages
                ]
                prompt_id, _, processed_messages = await asyncio.to_thread(
                    self._handle_database_operations,
                    dummy_func,
                    "lm_run",
                    model,
                    temperature,
                    processed_messages,
                )
                messages_use = processed_messages  # Use the processed messages from DB
            else:
                messages_use = messages

            if stream:
                # Return an async generator
                async def generator_wrapper():
                    async for chunk in self.process_messages_stream(
                        messages_use,
                        model,
                        temperature,
                        tools,
                        response_model,
                        use_db,
                        max_iterations,
                    ):
                        yield chunk

                return generator_wrapper()
            else:
                return await self.process_messages_sync(
                    messages_use,
                    model,
                    temperature,
                    tools,
                    response_model,
                    use_db,
                    max_iterations,
                    conversation,
                    prompt_id,
                )

        return _lm_run_impl()

    # Convenience methods for usage stats
    def get_total_cost(self) -> float:
        """Get total cost across all requests"""
        return self.usage.total_cost_usd

    def get_model_usage(self, model: str) -> Dict[str, float]:
        """Get usage statistics for a specific model"""
        return self.usage.model_usage.get(model, {})

    def get_usage_summary(self) -> Dict[str, Any]:
        """Get a complete summary of usage statistics"""
        return {
            "total_tokens": self.usage.total_tokens,
            "total_cost_usd": self.usage.total_cost_usd,
            "request_count": self.usage.request_count,
            "last_request": self.usage.last_request_time,
            "model_breakdown": self.usage.model_usage,
        }

    def reset_usage_stats(self):
        """Reset all usage statistics"""
        self.usage = UsageStats()

    def add_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """Add a tool function to the tool manager."""
        self.tool_manager.add_tool(func, name, description)

    def tool(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Callable[[Callable], Callable]:
        """Decorator to register a tool function."""
        return self.tool_manager.tool(name, description)

    @staticmethod
    def system(content: str) -> Message:
        """Create a system message."""
        return Message(role="system", content=dedent(content.strip()))

    @staticmethod
    def user(content: str) -> Message:
        """Create a user message."""
        return Message(role="user", content=dedent(content.strip()))

    @staticmethod
    def assistant(content: str) -> Message:
        """Create an assistant message."""
        return Message(role="assistant", content=dedent(content.strip()))


neat = Neat()
