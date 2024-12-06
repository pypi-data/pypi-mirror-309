"""Global context management"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any


class GlobalContext:
    """Global context manager"""

    def __init__(self) -> None:
        self._context: dict[str, Any] = {}
        self._defaults: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Set context value"""
        self._context[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get context value"""
        return self._context.get(key, self._defaults.get(key, default))

    @asynccontextmanager
    async def scope(self, **kwargs: Any) -> AsyncIterator["GlobalContext"]:
        """
        Create temporary context scope

        Args:
            **kwargs: Context values to set for this scope

        Returns:
            AsyncIterator[GlobalContext]: Context manager instance

        """
        old_values = {}
        for key, value in kwargs.items():
            old_values[key] = self._context.get(key)
            self._context[key] = value
        try:
            yield self
        finally:
            for key, value in old_values.items():
                if value is None:
                    del self._context[key]
                else:
                    self._context[key] = value


context = GlobalContext()
