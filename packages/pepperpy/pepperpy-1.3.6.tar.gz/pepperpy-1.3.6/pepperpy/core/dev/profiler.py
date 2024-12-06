"""Profiling utilities"""

import asyncio
import cProfile
import functools
import io
import pstats
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager, redirect_stdout
from typing import TypeVar, cast

from typing_extensions import ParamSpec

from pepperpy.core.logging import get_logger

T = TypeVar("T")
P = ParamSpec("P")


# Estendendo Stats para incluir os atributos que sabemos que existem
class ExtendedStats(pstats.Stats):
    total_calls: int
    total_tt: float


class AsyncProfiler:
    """Async function profiler"""

    def __init__(self, name: str):
        self.name = name
        self._profiler = cProfile.Profile()
        self._logger = get_logger(__name__)
        self._stats: dict[str, ExtendedStats] = {}

    @asynccontextmanager
    async def profile(self) -> AsyncIterator["AsyncProfiler"]:
        """
        Profile execution with detailed statistics

        Returns:
            AsyncIterator[AsyncProfiler]: Profiler instance

        """
        self._profiler.enable()
        try:
            yield self
        finally:
            self._profiler.disable()
            stats = cast(ExtendedStats, pstats.Stats(self._profiler))
            stats.sort_stats("cumulative")
            self._stats[self.name] = stats
            await self._logger.async_.debug(
                f"Profile stats for {self.name}",
                total_calls=stats.total_calls,
                total_time=stats.total_tt,
            )

    def profile_function(self, func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        """
        Decorator for profiling async functions

        Args:
            func: Function to profile

        Returns:
            Callable[P, Awaitable[T]]: Decorated function

        """
        if not asyncio.iscoroutinefunction(func):
            raise ValueError("Can only profile async functions")

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            profiler = AsyncProfiler(f"{func.__name__}_{id(func)}")
            async with profiler.profile():
                return await func(*args, **kwargs)

        return wrapper

    def print_stats(self, limit: int | None = None) -> None:
        """Print profiling statistics"""
        for name, stats in self._stats.items():
            print(f"\nProfile stats for {name}:")
            if limit is not None:
                stats.print_stats(limit)
            else:
                stats.print_stats()

    def get_stats(self) -> dict[str, ExtendedStats]:
        """Get raw profiling statistics"""
        return self._stats


class ProfileStats:
    def __init__(self, profiler: cProfile.Profile):
        self.profiler = profiler
        self._stats: ExtendedStats | None = None

    @property
    def stats(self) -> ExtendedStats:
        if self._stats is None:
            self._stats = cast(ExtendedStats, pstats.Stats(self.profiler))
        return self._stats

    def print_stats(self, amount: int | None = None) -> str:
        output = io.StringIO()
        stats = self.stats.sort_stats(pstats.SortKey.TIME)

        total_calls = stats.total_calls
        total_time = stats.total_tt

        output.write(f"Total calls: {total_calls}\n")
        output.write(f"Total time: {total_time:.3f}s\n\n")

        # Redirecionar a saída para o StringIO
        with redirect_stdout(output):
            if amount is not None:
                stats.print_stats(amount)
            else:
                stats.print_stats()

        return output.getvalue()
