"""Cache strategies implementation"""

from abc import ABC, abstractmethod
from typing import Any


class CacheStrategy(ABC):
    """Base class for cache strategies"""

    @abstractmethod
    async def get(self, key: str) -> Any | None:
        """Get cached value"""

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set cache value"""


class LRUStrategy(CacheStrategy):
    """Least Recently Used cache strategy"""



class LFUStrategy(CacheStrategy):
    """Least Frequently Used cache strategy"""

