"""Client for database operations"""

from .config import DatabaseConfig
from .types import QueryResult


class DatabaseClient:
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self._connection = None

    async def connect(self) -> None:
        """Establish database connection"""
        raise NotImplementedError

    async def disconnect(self) -> None:
        """Close database connection"""
        raise NotImplementedError

    async def execute_query(self, query: str) -> QueryResult:
        """Execute a database query"""
        raise NotImplementedError
