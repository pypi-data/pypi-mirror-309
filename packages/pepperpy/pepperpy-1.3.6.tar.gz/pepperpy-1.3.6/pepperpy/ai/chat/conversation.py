"""Chat conversation implementation"""

from collections.abc import AsyncIterator

from ..client import AIClient
from ..types import AIResponse
from .types import ChatRole


class Conversation:
    """Chat conversation manager"""

    def __init__(self, client: AIClient, system_prompt: str | None = None):
        """Initialize conversation with optional system prompt"""
        self.client = client
        self.messages: list[dict[str, str]] = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_message(self, role: ChatRole, content: str) -> None:
        """Add message to conversation history"""
        self.messages.append({"role": role, "content": content})

    def clear_history(self) -> None:
        """Clear conversation history"""
        system_message = next((msg for msg in self.messages if msg["role"] == "system"), None)
        self.messages.clear()
        if system_message:
            self.messages.append(system_message)

    async def send_message(self, content: str) -> AIResponse:
        """Send user message and get response"""
        self.add_message("user", content)
        response = await self.client.complete(self.messages)
        self.add_message("assistant", response.content)
        return response

    async def stream_message(self, content: str) -> AsyncIterator[AIResponse]:
        """Stream user message response"""
        self.add_message("user", content)
        async for response in self.client.stream(self.messages):
            if response.content.strip():
                yield response

        # Add final response to history
        if response.content.strip():
            self.add_message("assistant", response.content)

    def get_history(self) -> list[dict[str, str]]:
        """Get conversation history"""
        return self.messages.copy()
