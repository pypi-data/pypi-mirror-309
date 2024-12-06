"""Base embedding provider implementation"""

from abc import ABC, abstractmethod
from typing import List, Protocol, Sequence

from ..config import EmbeddingConfig
from ..types import EmbeddingResult


class EmbeddingProvider(Protocol):
    """Protocol for embedding providers"""
    
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding for text"""
        ...

    async def embed_batch(self, texts: List[str]) -> Sequence[EmbeddingResult]:
        """Generate embeddings for multiple texts"""
        ...


class BaseEmbeddingProvider(ABC):
    """Base class for embedding providers"""

    def __init__(self, config: EmbeddingConfig) -> None:
        """Initialize provider with configuration"""
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""

    @abstractmethod
    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embedding for text"""

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> Sequence[EmbeddingResult]:
        """Generate embeddings for multiple texts"""
