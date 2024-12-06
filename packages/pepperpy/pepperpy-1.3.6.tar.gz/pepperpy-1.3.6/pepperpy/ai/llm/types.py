"""LLM types and configurations"""

from dataclasses import dataclass, field
from typing import Any, Literal, TypedDict


class Message(TypedDict):
    """Chat message"""

    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class LLMResponse:
    """LLM response"""

    content: str
    model: str
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMConfig:
    """Base LLM configuration"""

    provider: Literal["openrouter", "stackspot", "openai"]
    api_key: str
    model: str

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.api_key:
            raise ValueError("API key is required")
        if not self.provider:
            raise ValueError("Provider is required")
