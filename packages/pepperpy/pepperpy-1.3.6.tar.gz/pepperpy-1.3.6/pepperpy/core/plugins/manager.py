"""Plugin system management"""

import importlib
import inspect
from pathlib import Path
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import PluginError, PluginLoadError


class PluginManager(BaseModule):
    """Manager for plugin discovery and loading"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="plugin_manager",
            version="1.0.0",
            description="Plugin system management",
            dependencies=[],
            config={},
        )
        self._plugins: dict[str, Any] = {}
        self._paths: list[str] = []

    async def _setup(self) -> None:
        """Initialize plugin manager"""

    async def _cleanup(self) -> None:
        """Cleanup plugin manager"""
        self._plugins.clear()
        self._paths.clear()

    def register(self, name: str, plugin: Any) -> None:
        """Register plugin"""
        self._plugins[name] = plugin

    def get_plugin(self, name: str) -> Any | None:
        """Get registered plugin"""
        return self._plugins.get(name)

    def add_search_path(self, path: str) -> None:
        """Add plugin search path"""
        if path not in self._paths:
            self._paths.append(path)

    async def discover(self) -> None:
        """Discover plugins in search paths"""
        for path in self._paths:
            try:
                plugin_path = Path(path)
                if not plugin_path.exists():
                    continue

                # Import all python files
                for file_path in plugin_path.glob("**/*.py"):
                    if file_path.name.startswith("_"):
                        continue

                    module_path = str(file_path.relative_to(plugin_path.parent)).replace("/", ".")
                    module_name = module_path[:-3]  # Remove .py

                    try:
                        module = importlib.import_module(module_name)

                        # Look for plugin classes/functions
                        for item in dir(module):
                            if item.startswith("_"):
                                continue

                            obj = getattr(module, item)
                            if hasattr(obj, "_plugin_name"):
                                self.register(obj._plugin_name, obj)

                    except Exception as e:
                        raise PluginLoadError(
                            f"Failed to load plugin module {module_name}: {e!s}", cause=e,
                        )

            except Exception as e:
                raise PluginError(f"Plugin discovery failed: {e!s}", cause=e)

    def get_plugins_by_type(self, plugin_type: type) -> list[Any]:
        """Get all plugins of specific type"""
        return [
            plugin
            for plugin in self._plugins.values()
            if inspect.isclass(plugin) and issubclass(plugin, plugin_type)
        ]


# Global plugin registry
registry = PluginManager()
