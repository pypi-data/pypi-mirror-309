"""Testing utilities"""

import asyncio
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any, TypeVar

from pepperpy.core.logging import get_logger

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class TestHelper:
    """Helper for async testing"""

    def __init__(self, name: str):
        self.name = name
        self._logger = get_logger(__name__)
        self._mocks = {}
        self._cleanup_funcs = []

    async def setup(self) -> None:
        """Setup test environment"""
        await self._logger.async_.info(f"Setting up test: {self.name}")

    async def teardown(self) -> None:
        """Cleanup test environment"""
        # Run cleanup functions in reverse order
        for cleanup in reversed(self._cleanup_funcs):
            try:
                await cleanup()
            except Exception as e:
                await self._logger.async_.error(f"Cleanup error: {e!s}")

        self._mocks.clear()
        self._cleanup_funcs.clear()

    def add_cleanup(self, func: Callable) -> None:
        """Add cleanup function"""
        self._cleanup_funcs.append(func)

    def mock(self, target: str, mock_obj: Any) -> None:
        """Register mock object"""
        self._mocks[target] = mock_obj

    def get_mock(self, target: str) -> Any | None:
        """Get registered mock"""
        return self._mocks.get(target)

    @asynccontextmanager
    async def assert_raises(self, expected: type[E]) -> AsyncIterator[None]:
        """
        Assert that code raises expected exception

        Args:
            expected: Expected exception type

        Returns:
            AsyncIterator[None]: Context manager

        Raises:
            AssertionError: If expected exception is not raised

        """
        try:
            yield
            raise AssertionError(f"Expected {expected.__name__} to be raised")
        except Exception as e:
            if not isinstance(e, expected):
                raise AssertionError(
                    f"Expected {expected.__name__}, but {type(e).__name__} was raised",
                ) from e

    @asynccontextmanager
    async def assert_not_raises(self) -> AsyncIterator[None]:
        """
        Assert that code does not raise any exceptions

        Returns:
            AsyncIterator[None]: Context manager

        Raises:
            AssertionError: If any exception is raised

        """
        try:
            yield
        except Exception as e:
            raise AssertionError(
                f"Expected no exceptions, but {type(e).__name__} was raised",
            ) from e

    async def assert_completes(self, coro: Callable, timeout: float = 1.0) -> None:
        """
        Assert that coroutine completes within timeout

        Args:
            coro: Coroutine to test
            timeout: Maximum time to wait in seconds

        Raises:
            AssertionError: If coroutine does not complete in time

        """
        try:
            await asyncio.wait_for(coro(), timeout=timeout)
        except TimeoutError:
            raise AssertionError(f"Operation did not complete within {timeout} seconds")
