"""Debugging utilities"""

import asyncio
import functools
import inspect
import sys
import traceback
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar, cast

from pepperpy.core.logging import get_logger

T = TypeVar("T")


class Debugger:
    """Debug context manager"""

    def __init__(self, name: str):
        self.name = name
        self._logger = get_logger(__name__)
        self._locals: dict[str, Any] = {}

    @contextmanager
    def debug(self) -> Iterator[None]:
        """
        Debug context

        Yields:
            Iterator[None]: Debug context

        """
        try:
            frame = inspect.currentframe()
            if frame is not None:
                caller = frame.f_back
                if caller is not None:
                    self._locals = dict(caller.f_locals)
            yield
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_traceback is not None:
                frames = traceback.extract_tb(exc_traceback)
                for frame in frames:
                    # Criar uma cópia local das informações do frame
                    error_info = {
                        "function": frame.name,
                        "line": frame.line,
                        "locals": self._locals.copy(),
                    }
                    # Usar uma função síncrona para logging
                    self._log_error(
                        f"Error in {frame.filename}:{frame.lineno}",
                        error_info,
                    )
            raise
        finally:
            self._locals.clear()

    def _log_error(self, message: str, error_info: dict[str, Any]) -> None:
        """Log error synchronously"""
        # Criar uma string formatada com todas as informações
        error_msg = (
            f"{message}\n"
            f"Function: {error_info['function']}\n"
            f"Line: {error_info['line']}\n"
            f"Local variables: {error_info['locals']}"
        )
        print(error_msg, file=sys.stderr)


def debug(name: str | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for debugging functions

    Args:
        name: Debug context name

    Returns:
        Callable[[Callable[..., T]], Callable[..., T]]: Decorated function

    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        debug_name = name or func.__name__

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            debugger = Debugger(debug_name)
            with debugger.debug():
                return func(*args, **kwargs)

        return wrapper

    return decorator


def debug_async(
    name: str | None = None,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """
    Decorator for debugging async functions

    Args:
        name: Debug context name

    Returns:
        Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]: Decorated function

    """

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        debug_name = name or func.__name__

        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            debugger = Debugger(debug_name)
            with debugger.debug():
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                    return cast(T, result)
                result = func(*args, **kwargs)
                return cast(T, result)

        return wrapper

    return decorator
