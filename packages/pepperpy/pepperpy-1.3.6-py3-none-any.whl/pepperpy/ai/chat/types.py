"""Chat types and models"""

from dataclasses import dataclass
from typing import Literal

ChatRole = Literal["system", "user", "assistant"]


@dataclass
class ChatMessage:
    """Represents a message in a chat conversation"""

    role: ChatRole
    content: str
    name: str | None = None
