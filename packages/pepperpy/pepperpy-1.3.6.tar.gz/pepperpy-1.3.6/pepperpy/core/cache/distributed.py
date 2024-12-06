"""Distributed cache implementation"""


import redis.asyncio as redis

from .exceptions import CacheConnectionError, CacheError


class DistributedCache:
    """Redis-based distributed cache"""

    def __init__(self, url: str):
        """
        Initialize distributed cache

        Args:
            url: Redis connection URL

        """
        self._url = url
        self._client: redis.Redis | None = None

    async def connect(self) -> None:
        """Connect to Redis server"""
        try:
            self._client = await redis.from_url(self._url)
            await self._client.ping()
        except Exception as e:
            raise CacheConnectionError(f"Failed to connect to Redis: {e!s}", cause=e)

    async def disconnect(self) -> None:
        """Disconnect from Redis server"""
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def get(self, key: str) -> str | None:
        """
        Get value from cache

        Args:
            key: Cache key

        Returns:
            Optional[str]: Cached value if exists

        """
        if self._client is None:
            raise CacheError("Not connected to Redis")

        try:
            value = await self._client.get(key)
            return value.decode("utf-8") if value else None
        except Exception as e:
            raise CacheError(f"Failed to get value: {e!s}", cause=e)

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        """
        Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        """
        if self._client is None:
            raise CacheError("Not connected to Redis")

        try:
            if ttl is not None:
                await self._client.setex(key, ttl, value)
            else:
                await self._client.set(key, value)
        except Exception as e:
            raise CacheError(f"Failed to set value: {e!s}", cause=e)

    async def delete(self, key: str) -> None:
        """
        Delete value from cache

        Args:
            key: Cache key

        """
        if self._client is None:
            raise CacheError("Not connected to Redis")

        try:
            await self._client.delete(key)
        except Exception as e:
            raise CacheError(f"Failed to delete value: {e!s}", cause=e)

    async def clear(self) -> None:
        """Clear all values from cache"""
        if self._client is None:
            raise CacheError("Not connected to Redis")

        try:
            await self._client.flushdb()
        except Exception as e:
            raise CacheError(f"Failed to clear cache: {e!s}", cause=e)
