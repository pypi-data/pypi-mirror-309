"""SQLite engine implementation"""

import time
from typing import Any

import aiosqlite

from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class SQLiteEngine(BaseEngine):
    """SQLite database engine"""

    async def initialize(self) -> None:
        """Initialize SQLite database"""
        try:
            self._pool = await aiosqlite.connect(
                database=self.config.database, timeout=self.config.timeout,
            )
            self._pool.row_factory = aiosqlite.Row
        except Exception as e:
            raise DatabaseError(f"Failed to initialize SQLite: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup SQLite resources"""
        if self._pool:
            await self._pool.close()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute SQLite query"""
        try:
            start_time = time.time()
            async with self._pool.execute(query, params or {}) as cursor:
                rows = await cursor.fetchall()
                await self._pool.commit()

                return QueryResult(
                    rows=[dict(row) for row in rows],
                    affected_rows=cursor.rowcount,
                    last_insert_id=cursor.lastrowid,
                    execution_time=time.time() - start_time,
                )
        except Exception as e:
            await self._pool.rollback()
            raise DatabaseError(f"SQLite query failed: {e!s}", cause=e)

    async def execute_many(
        self, query: str, params_list: list[dict[str, Any]],
    ) -> list[QueryResult]:
        """Execute multiple SQLite queries"""
        results = []
        async with self._pool.cursor() as cursor:
            try:
                for params in params_list:
                    start_time = time.time()
                    await cursor.execute(query, params)
                    rows = await cursor.fetchall()

                    results.append(
                        QueryResult(
                            rows=[dict(row) for row in rows],
                            affected_rows=cursor.rowcount,
                            last_insert_id=cursor.lastrowid,
                            execution_time=time.time() - start_time,
                        ),
                    )
                await self._pool.commit()
                return results
            except Exception as e:
                await self._pool.rollback()
                raise DatabaseError(f"SQLite batch query failed: {e!s}", cause=e)

    async def transaction(self) -> Any:
        """Get SQLite transaction context manager"""
        return self._pool
