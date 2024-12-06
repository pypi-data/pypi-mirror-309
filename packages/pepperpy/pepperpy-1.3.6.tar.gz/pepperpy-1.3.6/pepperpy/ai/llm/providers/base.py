"""Base LLM provider implementation"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Generic, TypeVar

from ..config import BaseConfig
from ..types import LLMResponse, Message

T = TypeVar("T", bound=BaseConfig)


class BaseLLMProvider(Generic[T], ABC):
    """Base class for LLM providers"""

    def __init__(self, config: T | None = None) -> None:
        """Initialize provider with configuration"""
        self._config: T | None = config

    @property
    def config(self) -> T:
        """Get provider configuration"""
        if not self._config:
            raise ValueError("Provider configuration is required")
        return self._config

    @config.setter
    def config(self, value: T | None) -> None:
        """Set provider configuration"""
        self._config = value

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""

    @abstractmethod
    async def complete(self, messages: list[Message]) -> LLMResponse:
        """Generate completion from messages"""

    @abstractmethod
    def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses from messages"""
        raise NotImplementedError("Stream method must be implemented by provider")
