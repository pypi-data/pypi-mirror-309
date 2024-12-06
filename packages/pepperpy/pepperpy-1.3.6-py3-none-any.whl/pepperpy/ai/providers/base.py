"""Base AI provider implementation"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from ..types import LLMResponse, Message


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the provider"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""

    @abstractmethod
    async def generate(self, messages: list[Message]) -> LLMResponse:
        """Generate a response from the LLM"""

    @abstractmethod
    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from the LLM"""
