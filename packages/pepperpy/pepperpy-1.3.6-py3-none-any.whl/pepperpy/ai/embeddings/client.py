"""Embedding client implementation"""

from dataclasses import asdict
from typing import Any, Dict, List, Optional, Sequence, cast

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import EmbeddingConfig
from .exceptions import EmbeddingError
from .providers import get_provider
from .providers.base import BaseEmbeddingProvider, EmbeddingProvider
from .types import EmbeddingResult


class EmbeddingClient(BaseModule):
    """Client for embedding operations"""

    def __init__(self, config: Optional[EmbeddingConfig] = None) -> None:
        super().__init__()
        self._config: EmbeddingConfig = config or EmbeddingConfig(
            model_name="all-MiniLM-L6-v2",
            provider="sentence_transformers",
        )
        self.metadata = ModuleMetadata(
            name="embeddings",
            version="1.0.0",
            description="Text embedding operations",
            dependencies=[],
            config=self._get_config_dict(),
        )
        self._provider: Optional[EmbeddingProvider] = None

    def _get_config_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary safely"""
        if isinstance(self._config, EmbeddingConfig):
            return asdict(self._config)
        return {}

    async def _setup(self) -> None:
        """Initialize embedding provider"""
        try:
            if not self._config:
                raise EmbeddingError("Embedding configuration is required")
            provider = get_provider(self._config)
            if isinstance(provider, BaseEmbeddingProvider):
                await provider.initialize()
                self._provider = provider
            else:
                raise EmbeddingError("Invalid provider type")
        except Exception as e:
            raise EmbeddingError("Failed to initialize embedding provider", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup embedding resources"""
        if isinstance(self._provider, BaseEmbeddingProvider):
            await self._provider.cleanup()

    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding for text"""
        if not self._provider:
            raise EmbeddingError("Embedding provider not initialized")
        try:
            return await self._provider.embed(text)
        except Exception as e:
            raise EmbeddingError(f"Failed to generate embedding: {e!s}", cause=e)

    async def embed_batch(self, texts: List[str]) -> Sequence[EmbeddingResult]:
        """Generate embeddings for multiple texts"""
        if not self._provider:
            raise EmbeddingError("Embedding provider not initialized")
        try:
            results = await self._provider.embed_batch(texts)
            return cast(Sequence[EmbeddingResult], results)
        except Exception as e:
            raise EmbeddingError(f"Failed to generate batch embeddings: {e!s}", cause=e)


# Global embedding client instance
embeddings = EmbeddingClient()
