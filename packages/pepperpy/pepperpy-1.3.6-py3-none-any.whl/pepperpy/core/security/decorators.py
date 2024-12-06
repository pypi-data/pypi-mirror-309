"""Security decorators implementation"""

import functools
from collections.abc import Callable
from typing import Any, TypeVar, cast

from .exceptions import AuthError

T = TypeVar("T", bound=Callable[..., Any])


def require_permission(permission: str) -> Callable[[T], T]:
    """
    Require specific permission to access function

    Args:
        permission: Required permission name

    Returns:
        Callable[[T], T]: Decorated function

    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .context import security_context

            if not await security_context.has_permission(permission):
                raise AuthError(f"Missing required permission: {permission}")
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_role(role: str) -> Callable[[T], T]:
    """
    Require specific role to access function

    Args:
        role: Required role name

    Returns:
        Callable[[T], T]: Decorated function

    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .context import security_context

            if not await security_context.has_role(role):
                raise AuthError(f"Missing required role: {role}")
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def authenticated() -> Callable[[T], T]:
    """
    Require authentication to access function

    Returns:
        Callable[[T], T]: Decorated function

    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .context import security_context

            if not await security_context.is_authenticated():
                raise AuthError("Authentication required")
            return await func(*args, **kwargs)

        return cast(T, wrapper)

    return decorator


def require_any_role(roles: list[str]) -> Callable[[T], T]:
    """
    Require any of the specified roles to access function

    Args:
        roles: List of acceptable roles

    Returns:
        Callable[[T], T]: Decorated function

    """

    def decorator(func: T) -> T:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            from .context import security_context

            for role in roles:
                if await security_context.has_role(role):
                    return await func(*args, **kwargs)
            raise AuthError(f"Missing any required role: {roles}")

        return cast(T, wrapper)

    return decorator
