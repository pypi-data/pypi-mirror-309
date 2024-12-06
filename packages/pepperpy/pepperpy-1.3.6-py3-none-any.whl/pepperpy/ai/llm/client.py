"""LLM client implementation"""

from collections.abc import AsyncIterator

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import LLMError
from .factory import ProviderConfig, ProviderFactory
from .types import LLMResponse, Message


class LLMClient(BaseModule):
    """Client for language model operations"""

    def __init__(self, config: ProviderConfig | None = None) -> None:
        """
        Initialize LLM client

        Args:
            config: Provider configuration

        """
        super().__init__()
        self._config: ProviderConfig | None = None
        self._provider = None

        # Configurar o módulo
        self.metadata = ModuleMetadata(
            name="llm",
            version="1.0.0",
            description="Language model operations",
            dependencies=[],
            config=config.to_dict() if config else {},
        )

        # Configurar o provider após metadata para evitar problemas de tipagem
        if config:
            self._config = config

    @property
    def config(self) -> ProviderConfig | None:
        """Get provider configuration"""
        return self._config

    async def _setup(self) -> None:
        """Initialize LLM provider"""
        try:
            if not self._config:
                raise LLMError("Configuration is required")

            # Usar o provider type do config para criar o provider
            provider_type = self._config.provider
            self._provider = ProviderFactory.get_provider(provider_type, self._config)
            try:
                await self._provider.initialize()
            except Exception as e:
                raise LLMError(f"Provider initialization failed: {e!s}", cause=e)
        except Exception as e:
            raise LLMError(f"Failed to initialize LLM provider: {e!s}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup LLM resources"""
        if self._provider:
            await self._provider.cleanup()

    async def complete(self, messages: list[Message]) -> LLMResponse:
        """
        Generate completion from messages

        Args:
            messages: List of messages to process

        Returns:
            LLMResponse: Generated response

        Raises:
            LLMError: If provider is not initialized or completion fails

        """
        if not self._provider:
            raise LLMError("LLM provider not initialized")
        return await self._provider.complete(messages)

    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """
        Stream responses from messages

        Args:
            messages: List of messages to process

        Yields:
            LLMResponse: Generated response chunks

        Raises:
            LLMError: If provider is not initialized or streaming fails

        """
        if not self._provider:
            raise LLMError("LLM provider not initialized")

        try:
            async for response in self._provider.stream(messages):
                yield response
        except Exception as e:
            raise LLMError(f"Failed to stream responses: {e!s}", cause=e)


# Global client instance
client = LLMClient()
