"""Base AutoGen agent implementation"""

from abc import ABC, abstractmethod
from typing import Any

from ...client import AIClient
from ...types import AIResponse, Message


class AutoGenAgent(ABC):
    """Base class for AutoGen agents"""

    def __init__(
        self,
        name: str,
        role: str,
        instructions: str,
        client: AIClient | None = None,
        **kwargs: Any,
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.client = client
        self.context: list[Message] = []
        self.metadata: dict[str, Any] = kwargs.get("metadata", {})

    async def send(self, content: str) -> AIResponse:
        """Send message and get response"""
        if not self.client:
            raise ValueError("Client is required for sending messages")

        message = Message(content=content, sender=self.name)
        self.context.append(message)
        return await self._generate_response(message)

    @abstractmethod
    async def _generate_response(self, message: Message) -> AIResponse:
        """Generate response to message"""
        raise NotImplementedError("Agents must implement _generate_response")

    def add_to_context(self, message: Message) -> None:
        """Add message to context"""
        self.context.append(message)

    def clear_context(self) -> None:
        """Clear conversation context"""
        self.context.clear()

    def get_context(self) -> list[Message]:
        """Get current context"""
        return self.context

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}')"
