"""AI module types and data structures"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class UsageInfo:
    """Token usage information"""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class AIResponse:
    """AI response with metadata"""

    content: str
    model: str
    usage: UsageInfo
    metadata: dict[str, str] | None = None


@dataclass
class Message:
    """Chat message"""

    content: str
    sender: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """LLM response data"""

    content: str
    model: str
    usage: dict[str, int] | None = None
    metadata: dict[str, str] | None = None
