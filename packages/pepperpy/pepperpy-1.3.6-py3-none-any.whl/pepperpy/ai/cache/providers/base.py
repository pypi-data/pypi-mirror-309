"""Base cache provider implementation"""

from abc import ABC, abstractmethod
from typing import Any

from ..config import CacheConfig


class BaseCacheProvider(ABC):
    """Base class for cache providers"""

    def __init__(self, config: CacheConfig):
        self.config = config

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup provider resources"""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Get value from cache"""

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete value from cache"""

    @abstractmethod
    async def clear(self) -> None:
        """Clear all values from cache"""
