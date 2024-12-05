# models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


@dataclass
class UsageStats:
    """Tracks usage statistics for LLM interactions"""
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    request_count: int = 0
    last_request_time: Optional[datetime] = None
    # Store usage per model
    model_usage: Dict[str, Dict[str, float]] = field(default_factory=lambda: {})
    
    def update(self, model: str, prompt_tokens: int, completion_tokens: int, cost: float):
        """Update usage statistics with new request data"""
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += (prompt_tokens + completion_tokens)
        self.total_cost_usd += cost
        self.request_count += 1
        self.last_request_time = datetime.now()
        
        if model not in self.model_usage:
            self.model_usage[model] = {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
                "cost_usd": 0.0,
                "requests": 0
            }
        
        model_stats = self.model_usage[model]
        model_stats["prompt_tokens"] += prompt_tokens
        model_stats["completion_tokens"] += completion_tokens
        model_stats["total_tokens"] += (prompt_tokens + completion_tokens)
        model_stats["cost_usd"] += cost
        model_stats["requests"] += 1

class StreamResult(BaseModel):
    """Container for the final streaming result and usage data."""
    content: str
    usage: 'UsageData'

class UsageData(BaseModel):
    """Represents token usage data from LLM responses."""
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None

    model_config = ConfigDict(extra="forbid")
class ExecutionData(BaseModel):
    version_id: int
    prompt_tokens: int
    completion_tokens: int
    execution_time: float
    usage: Optional[UsageData] = None

    model_config = ConfigDict(extra="forbid")

class PromptData(BaseModel):
    id: Optional[int] = None
    func_name: str
    version: int
    hash: str
    model: str
    temperature: float
    prompt: str
    environment: str

    model_config = ConfigDict(extra="forbid")

class FunctionCall(BaseModel):
    name: str
    arguments: str

class ToolCall(BaseModel):
    id: str
    type: str = "function"
    function: FunctionCall

class Message(BaseModel):
    role: str
    content: Optional[str] = None
    name: Optional[str] = None
    function_call: Optional[FunctionCall] = None
    tool_calls: Optional[List[ToolCall]] = None
    tool_call_id: Optional[str] = None
    usage: Optional[UsageData] = None

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "examples": [
                {"role": "user", "content": "Hello, how are you?"},
                {
                    "role": "assistant",
                    "content": "I'm doing well, thank you for asking!",
                    "tool_calls": [
                        {
                            "id": "call_abc123",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "New York"}',
                            },
                        }
                    ],
                },
                {
                    "role": "tool",
                    "tool_call_id": "call_abc123",
                    "name": "get_weather",
                    "content": "The weather in New York is sunny with a high of 75°F.",
                },
            ]
        },
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        return cls(**data)

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        allowed_roles = {"system", "user", "assistant", "tool"}
        if v not in allowed_roles:
            raise ValueError(
                f"Invalid role. Must be one of: {', '.join(allowed_roles)}"
            )
        return v
