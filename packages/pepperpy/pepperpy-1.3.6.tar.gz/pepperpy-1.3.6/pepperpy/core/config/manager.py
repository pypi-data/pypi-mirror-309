"""Configuration management implementation"""

from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import ConfigError
from .types import ConfigFormat, ConfigSource


class ConfigManager(BaseModule):
    """Manager for configuration files"""

    def __init__(self):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="config_manager",
            version="1.0.0",
            description="Configuration management",
            dependencies=[],
            config={},
        )
        self._configs: dict[str, dict[str, Any]] = {}
        self._sources: dict[str, ConfigSource] = {}
        self._watchers: dict[str, Callable[[dict[str, Any]], None]] = {}

    async def _setup(self) -> None:
        """Initialize config manager"""

    async def _cleanup(self) -> None:
        """Cleanup config resources"""
        self._configs.clear()
        self._sources.clear()
        self._watchers.clear()

    async def load_config(
        self, name: str, file_path: str | Path, format: ConfigFormat | None = None,
    ) -> dict[str, Any]:
        """Load configuration from file"""
        try:
            file_path = Path(file_path)
            if not format:
                format = ConfigFormat(file_path.suffix[1:])

            # Load and parse config
            with file_path.open() as f:
                if format == ConfigFormat.YAML:
                    config = yaml.safe_load(f)
                else:
                    raise ConfigError(f"Unsupported format: {format}")

            self._configs[name] = config
            self._sources[name] = ConfigSource(
                name=name,
                path=file_path,
                format=format,
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
            )
            return config

        except Exception as e:
            raise ConfigError(f"Failed to load config: {e!s}", cause=e)

    async def save_config(
        self, name: str, config: dict[str, Any], file_path: str | Path,
    ) -> None:
        """Save configuration to file"""
        try:
            file_path = Path(file_path)
            format = ConfigFormat(file_path.suffix[1:])

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Save config
            with file_path.open("w") as f:
                if format == ConfigFormat.YAML:
                    yaml.safe_dump(config, f)
                else:
                    raise ConfigError(f"Unsupported format: {format}")

            self._configs[name] = config
            self._sources[name] = ConfigSource(
                name=name,
                path=file_path,
                format=format,
                last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
            )

        except Exception as e:
            raise ConfigError(f"Failed to save config: {e!s}", cause=e)

    def get_config(self, name: str) -> dict[str, Any] | None:
        """Get loaded configuration"""
        return self._configs.get(name)

    async def watch_config(self, name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        """Watch configuration for changes"""
        if name not in self._sources:
            raise ConfigError(f"Config not loaded: {name}")

        source = self._sources[name]
        if not source.path:
            raise ConfigError(f"Config has no file path: {name}")

        current_mtime = datetime.fromtimestamp(source.path.stat().st_mtime)

        if source.last_modified and current_mtime > source.last_modified:
            config = await self.load_config(name, source.path, source.format)
            callback(config)
            source.last_modified = current_mtime

    def get_config_path(self, name: str) -> Path | None:
        """Get configuration file path"""
        source = self._sources.get(name)
        return source.path if source else None


# Global config manager instance
config_manager = ConfigManager()
