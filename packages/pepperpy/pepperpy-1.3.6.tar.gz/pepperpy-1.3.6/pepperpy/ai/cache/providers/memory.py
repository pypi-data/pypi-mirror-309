"""Memory cache provider implementation"""

from datetime import datetime, timedelta
from typing import Any

from ..config import CacheConfig
from ..exceptions import CacheError
from .base import BaseCacheProvider


class MemoryCacheProvider(BaseCacheProvider):
    """In-memory cache provider"""

    def __init__(self, config: CacheConfig):
        super().__init__(config)
        self._cache: dict[str, tuple[Any, datetime | None]] = {}

    async def initialize(self) -> None:
        """Initialize provider"""

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        self._cache.clear()

    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        if key not in self._cache:
            return None

        value, expires_at = self._cache[key]
        if expires_at and datetime.utcnow() > expires_at:
            await self.delete(key)
            return None

        return value

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        try:
            expires_at = None
            if ttl is not None:
                expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            elif self.config.ttl > 0:
                expires_at = datetime.utcnow() + timedelta(seconds=self.config.ttl)

            self._cache[key] = (value, expires_at)

            # Verificar limite de tamanho
            if self.config.max_size > 0 and len(self._cache) > self.config.max_size:
                # Remover itens mais antigos
                sorted_items = sorted(
                    self._cache.items(),
                    key=lambda x: x[1][1] or datetime.max,
                )
                for old_key, _ in sorted_items[: len(self._cache) - self.config.max_size]:
                    del self._cache[old_key]

        except Exception as e:
            raise CacheError(f"Failed to set cache value: {e!s}", cause=e)

    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear all values from cache"""
        self._cache.clear()
