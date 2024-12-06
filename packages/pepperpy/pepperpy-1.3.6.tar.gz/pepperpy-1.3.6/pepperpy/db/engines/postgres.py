"""PostgreSQL engine implementation"""

import time
from typing import Any

import asyncpg

from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class PostgresEngine(BaseEngine):
    """PostgreSQL database engine"""

    async def initialize(self) -> None:
        """Initialize PostgreSQL database"""
        try:
            self._pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port or 5432,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password,
                min_size=1,
                max_size=self.config.pool_size,
                **self.config.params,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to initialize PostgreSQL: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup PostgreSQL resources"""
        if self._pool:
            await self._pool.close()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute PostgreSQL query"""
        if not self._pool:
            raise DatabaseError("Database connection not initialized")

        async with self._pool.acquire() as connection:
            try:
                start_time = time.time()
                result = await connection.fetch(query, *(params or {}).values())

                return QueryResult(
                    rows=[dict(row) for row in result],
                    affected_rows=len(result),
                    execution_time=time.time() - start_time,
                )
            except Exception as e:
                raise DatabaseError(f"PostgreSQL query failed: {e!s}", cause=e)

    async def execute_many(
        self, query: str, params_list: list[dict[str, Any]],
    ) -> list[QueryResult]:
        """Execute multiple PostgreSQL queries"""
        if not self._pool:
            raise DatabaseError("Database connection not initialized")

        async with self._pool.acquire() as connection:
            try:
                results = []
                for params in params_list:
                    start_time = time.time()
                    result = await connection.fetch(query, *params.values())

                    results.append(
                        QueryResult(
                            rows=[dict(row) for row in result],
                            affected_rows=len(result),
                            execution_time=time.time() - start_time,
                        ),
                    )
                return results
            except Exception as e:
                raise DatabaseError(f"PostgreSQL batch query failed: {e!s}", cause=e)

    async def transaction(self) -> Any:
        """Get PostgreSQL transaction context manager"""
        return self._pool
