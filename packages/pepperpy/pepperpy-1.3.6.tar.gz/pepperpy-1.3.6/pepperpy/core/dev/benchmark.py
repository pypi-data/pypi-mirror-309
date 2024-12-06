"""Benchmarking utilities"""

import asyncio
import time
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, TypeVar, cast

from pepperpy.core.logging import get_logger

T = TypeVar("T")


@dataclass
class BenchmarkResult:
    """Benchmark result data"""

    name: str
    elapsed: float
    iterations: int
    metadata: dict[str, Any]


class Benchmark:
    """Benchmark runner"""

    def __init__(self, name: str):
        self.name = name
        self._logger = get_logger(__name__)
        self._start_time: float = 0
        self._end_time: float = 0

    @asynccontextmanager
    async def run(self) -> AsyncGenerator[BenchmarkResult, None]:
        """
        Run benchmark

        Yields:
            AsyncGenerator[BenchmarkResult, None]: Benchmark result

        """
        self._start_time = time.perf_counter()
        try:
            result = BenchmarkResult(
                name=self.name,
                elapsed=0.0,
                iterations=1,
                metadata={},
            )
            yield result
        finally:
            self._end_time = time.perf_counter()
            result.elapsed = self._end_time - self._start_time
            await self._logger.async_.debug(
                f"Benchmark {self.name} completed",
                elapsed=result.elapsed,
                iterations=result.iterations,
            )


def benchmark(name: str) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Decorator for benchmarking functions

    Args:
        name: Benchmark name

    Returns:
        Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]: Decorated function

    """

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            bench = Benchmark(name)
            async with bench.run():
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
            return cast(T, result)

        return wrapper

    return decorator
