"""Cache manager implementation"""

from typing import Any, TypeVar

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import CacheConfig
from .exceptions import CacheError
from .providers.base import BaseCacheProvider
from .providers.memory import MemoryCacheProvider

KT = TypeVar("KT")
VT = TypeVar("VT")


class CacheManager(BaseModule):
    """Manager for cache operations"""

    _config: CacheConfig | None
    _provider: BaseCacheProvider | None

    def __init__(self, config: CacheConfig | None = None):
        super().__init__()
        self._config = config or CacheConfig()
        self.metadata = ModuleMetadata(
            name="cache",
            version="1.0.0",
            description="Cache operations",
            dependencies=[],
            config=self._config.dict(),
        )
        self._provider = None

    async def _setup(self) -> None:
        """Initialize cache provider"""
        try:
            if not self._config:
                raise CacheError("Cache configuration is required")
            self._provider = MemoryCacheProvider(self._config)
            await self._provider.initialize()
        except Exception as e:
            raise CacheError("Failed to initialize cache provider", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup cache resources"""
        if self._provider:
            await self._provider.cleanup()

    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        if not self._provider:
            raise CacheError("Cache provider not initialized")
        return await self._provider.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        if not self._provider:
            raise CacheError("Cache provider not initialized")
        await self._provider.set(key, value, ttl)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if not self._provider:
            raise CacheError("Cache provider not initialized")
        await self._provider.delete(key)

    async def clear(self) -> None:
        """Clear all values from cache"""
        if not self._provider:
            raise CacheError("Cache provider not initialized")
        await self._provider.clear()


# Global cache manager instance
cache = CacheManager()
