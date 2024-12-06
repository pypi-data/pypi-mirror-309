"""In-memory cache implementation"""

from datetime import datetime, timedelta
from typing import Any, Generic, TypeVar

from .exceptions import CacheError

KT = TypeVar("KT")
VT = TypeVar("VT")


class MemoryCache(Generic[KT, VT]):
    """Simple in-memory cache implementation"""

    def __init__(self):
        self._cache: dict[KT, dict[str, Any]] = {}

    def get(self, key: KT) -> VT | None:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Optional[VT]: Cached value if exists

        """
        try:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            if "expires_at" in entry and datetime.now() >= entry["expires_at"]:
                del self._cache[key]
                return None

            return entry["value"]
        except Exception as e:
            raise CacheError(f"Failed to get value: {e!s}", cause=e)

    def set(self, key: KT, value: VT, ttl: int | None = None) -> None:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        """
        try:
            entry: dict[str, Any] = {"value": value}
            if ttl is not None:
                entry["expires_at"] = datetime.now() + timedelta(seconds=ttl)
            self._cache[key] = entry
        except Exception as e:
            raise CacheError(f"Failed to set value: {e!s}", cause=e)

    def delete(self, key: KT) -> None:
        """
        Delete value from cache

        Args:
            key: Cache key

        """
        try:
            if key in self._cache:
                del self._cache[key]
        except Exception as e:
            raise CacheError(f"Failed to delete value: {e!s}", cause=e)

    def clear(self) -> None:
        """Clear all values from cache"""
        try:
            self._cache.clear()
        except Exception as e:
            raise CacheError(f"Failed to clear cache: {e!s}", cause=e)

    def __contains__(self, key: KT) -> bool:
        """Check if key exists in cache"""
        return key in self._cache and (
            "expires_at" not in self._cache[key] or datetime.now() < self._cache[key]["expires_at"]
        )

    def __len__(self) -> int:
        """Get current cache size"""
        return len(self._cache)
