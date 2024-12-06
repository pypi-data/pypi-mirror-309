"""DuckDB engine implementation"""

import time
from typing import Any

import duckdb

from ..exceptions import DatabaseError
from ..types import QueryResult
from .base import BaseEngine


class DuckDBEngine(BaseEngine):
    """DuckDB database engine"""

    async def initialize(self) -> None:
        """Initialize DuckDB database"""
        try:
            self._pool = duckdb.connect(
                database=self.config.database, read_only=False, **self.config.params,
            )
        except Exception as e:
            raise DatabaseError(f"Failed to initialize DuckDB: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup DuckDB resources"""
        if self._pool:
            self._pool.close()

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute DuckDB query"""
        if not self._pool:
            raise DatabaseError("Database connection not initialized")

        try:
            start_time = time.time()
            result = self._pool.execute(query, parameters=params or {}).fetchall()

            # Converter os resultados para dicionários com chaves str
            rows = [{str(k): v for k, v in row.items()} for row in result]

            return QueryResult(
                rows=rows,
                affected_rows=len(result),
                execution_time=time.time() - start_time,
            )
        except Exception as e:
            raise DatabaseError(f"DuckDB query failed: {e!s}", cause=e)

    async def execute_many(
        self, query: str, params_list: list[dict[str, Any]],
    ) -> list[QueryResult]:
        """Execute multiple DuckDB queries"""
        if not self._pool:
            raise DatabaseError("Database connection not initialized")

        try:
            results = []
            for params in params_list:
                start_time = time.time()
                result = self._pool.execute(query, parameters=params).fetchall()

                # Converter os resultados para dicionários com chaves str
                rows = [{str(k): v for k, v in row.items()} for row in result]

                results.append(
                    QueryResult(
                        rows=rows,
                        affected_rows=len(result),
                        execution_time=time.time() - start_time,
                    ),
                )
            return results
        except Exception as e:
            raise DatabaseError(f"DuckDB batch query failed: {e!s}", cause=e)

    async def transaction(self) -> Any:
        """Get DuckDB transaction context manager"""
        return self._pool
