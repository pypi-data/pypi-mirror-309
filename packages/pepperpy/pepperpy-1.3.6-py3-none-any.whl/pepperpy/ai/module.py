"""AI module implementation"""

from collections.abc import AsyncIterator
from dataclasses import asdict
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import AIConfig
from .exceptions import AIError
from .providers.base import BaseLLMProvider
from .types import LLMResponse, Message


class AIModule(BaseModule):
    """Main AI module implementation"""

    def __init__(self, config: AIConfig | None = None):
        super().__init__()
        config_dict = asdict(config) if config else {}
        self.metadata = ModuleMetadata(
            name="ai",
            version="1.0.0",
            description="AI functionality",
            dependencies=[],
            config=config_dict,
        )
        self._provider: BaseLLMProvider | None = None
        self._initialized: bool = False

    async def _setup(self) -> None:
        """Setup the AI module"""
        # TODO: Initialize provider based on configuration
        self._provider = None  # Replace with actual provider initialization
        self._initialized = True

    async def _cleanup(self) -> None:
        """Cleanup the AI module"""
        if self._provider:
            await self._provider.cleanup()
        self._initialized = False

    async def __aenter__(self) -> "AIModule":
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.cleanup()

    async def generate(self, messages: list[Message]) -> LLMResponse:
        """Generate a response using the configured LLM provider"""
        if not self._initialized:
            raise AIError("AI module not initialized")

        if not self._provider:
            raise AIError("No LLM provider configured")

        return await self._provider.generate(messages)

    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream responses using the configured LLM provider"""
        if not self._initialized:
            raise AIError("AI module not initialized")

        if not self._provider:
            raise AIError("No LLM provider configured")

        provider = self._provider  # Store in local variable to satisfy type checker

        async def stream_wrapper() -> AsyncIterator[LLMResponse]:
            async for response in await provider.stream(messages):
                yield response

        return stream_wrapper()

    def get_config(self) -> dict[str, Any]:
        """Get the module configuration"""
        if not self.metadata or not isinstance(self.metadata.config, dict):
            return {}
        return self.metadata.config
