"""Core configuration module"""

from dataclasses import dataclass, field
from typing import Any

from .config import Config, load_config


@dataclass
class ModuleConfig:
    """Base module configuration"""

    name: str
    version: str
    debug: bool = False
    description: str | None = None
    dependencies: list[str] | None = None
    config: dict[str, Any] = field(default_factory=dict)


__all__ = ["ModuleConfig", "Config", "load_config"]
