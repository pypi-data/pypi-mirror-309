"""Base module implementation"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class ModuleMetadata:
    """Module metadata container"""

    name: str
    version: str
    description: str
    dependencies: list[str]
    config: dict[str, Any]


class ModuleStatus(Enum):
    """Module status"""

    INACTIVE = "inactive"
    ACTIVE = "active"
    ERROR = "error"


class BaseModule(ABC):
    """Base class for all modules"""

    def __init__(self) -> None:
        self._config: dict[str, Any] | None = None
        self._status: ModuleStatus = ModuleStatus.INACTIVE
        self.metadata: ModuleMetadata | None = None

    @property
    def config(self) -> dict[str, Any]:
        """Get module configuration"""
        if not self._config:
            raise ValueError("Module configuration not set")
        return self._config

    @config.setter
    def config(self, value: dict[str, Any]) -> None:
        """Set module configuration"""
        self._config = value

    @property
    def status(self) -> ModuleStatus:
        """Get module status"""
        return self._status

    async def initialize(self) -> None:
        """Initialize module"""
        await self._setup()

    async def cleanup(self) -> None:
        """Cleanup module resources"""
        await self._cleanup()

    @abstractmethod
    async def _setup(self) -> None:
        """Module-specific initialization"""

    @abstractmethod
    async def _cleanup(self) -> None:
        """Module-specific cleanup"""
