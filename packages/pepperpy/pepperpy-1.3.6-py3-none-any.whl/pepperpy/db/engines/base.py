"""Base database engine implementation"""

from abc import ABC, abstractmethod
from typing import Any

from ..config import DatabaseConfig
from ..types import QueryResult


class BaseEngine(ABC):
    """Base class for database engines"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._pool = None

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize database engine"""

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup database resources"""

    @abstractmethod
    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""

    @abstractmethod
    async def execute_many(
        self, query: str, params_list: list[dict[str, Any]],
    ) -> list[QueryResult]:
        """Execute multiple queries"""

    @abstractmethod
    async def transaction(self) -> Any:
        """Get transaction context manager"""
