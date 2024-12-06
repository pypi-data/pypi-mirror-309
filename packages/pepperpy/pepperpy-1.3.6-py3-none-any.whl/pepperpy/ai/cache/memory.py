"""Memory cache implementation"""

import asyncio
import time
from collections import OrderedDict
from typing import Any

from .exceptions import CacheError


class MemoryCache:
    """Thread-safe memory cache with TTL"""

    def __init__(self, default_ttl: int = 3600):
        self._cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._default_ttl = default_ttl
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        try:
            async with self._lock:
                if key not in self._cache:
                    return None

                entry = self._cache[key]
                if entry.get("expires_at") and time.time() > entry["expires_at"]:
                    del self._cache[key]
                    return None

                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return entry["value"]
        except Exception as e:
            raise CacheError(f"Failed to get from cache: {e!s}", cause=e)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        try:
            async with self._lock:
                expires_at = time.time() + (ttl or self._default_ttl)
                self._cache[key] = {
                    "value": value,
                    "expires_at": expires_at,
                    "created_at": time.time(),
                }
                self._cache.move_to_end(key)
        except Exception as e:
            raise CacheError(f"Failed to set in cache: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Remove expired entries"""
        try:
            async with self._lock:
                now = time.time()
                expired = [
                    key
                    for key, entry in self._cache.items()
                    if entry.get("expires_at") and entry["expires_at"] <= now
                ]
                for key in expired:
                    del self._cache[key]
        except Exception as e:
            raise CacheError(f"Cache cleanup failed: {e!s}", cause=e)
