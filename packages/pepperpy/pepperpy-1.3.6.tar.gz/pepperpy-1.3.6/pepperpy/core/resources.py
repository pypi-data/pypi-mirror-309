"""Resource management utilities"""

import inspect
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar, Union, overload

T = TypeVar("T")
ResourceType = Union[str, Path, type[Any], Callable[..., Any]]


def get_resource_path(resource: ResourceType) -> Path:
    """
    Get path to a resource

    Args:
        resource: Resource to get path for. Can be:
            - A string path
            - A Path object
            - A class
            - A function/method

    Returns:
        Path: Path to the resource

    """
    if isinstance(resource, (str, Path)):
        return Path(resource)

    if inspect.isclass(resource) or inspect.isfunction(resource):
        module = inspect.getmodule(resource)
        if module is None:
            raise ValueError(f"Could not determine module for {resource}")
        module_file = getattr(module, "__file__", None)
        if module_file is None:
            raise ValueError(f"Could not determine file for module of {resource}")
        return Path(module_file).parent

    raise ValueError(f"Invalid resource type: {type(resource)}")


class ResourceManager:
    """Resource manager for handling file paths and module locations"""

    def __init__(self, base_path: str | Path | None = None):
        """
        Initialize resource manager

        Args:
            base_path: Base path for resolving relative paths. Defaults to current directory.

        """
        self.base_path = Path(base_path or Path.cwd())
        self._paths: dict[str, Path] = {}

    def register(self, name: str, resource: ResourceType) -> None:
        """
        Register a resource path

        Args:
            name: Name to register resource as
            resource: Resource to register. Can be:
                - A string path
                - A Path object
                - A class
                - A function/method

        """
        path = get_resource_path(resource)
        if not path.is_absolute():
            path = self.base_path / path
        self._paths[name] = path

    @overload
    def get(self, name: str) -> Path: ...

    @overload
    def get(self, name: str, as_str: bool) -> str | Path: ...

    def get(self, name: str, as_str: bool = False) -> str | Path:
        """
        Get path to a registered resource

        Args:
            name: Name of registered resource
            as_str: Return path as string instead of Path object

        Returns:
            Union[str, Path]: Path to resource

        Raises:
            KeyError: If resource is not registered

        """
        if name not in self._paths:
            raise KeyError(f"Resource not registered: {name}")

        path = self._paths[name]
        return str(path) if as_str else path

    def __contains__(self, name: str) -> bool:
        """
        Check if resource is registered

        Args:
            name: Name of resource to check

        Returns:
            bool: True if resource is registered

        """
        return name in self._paths
