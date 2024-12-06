"""Core module initialization"""

from .exceptions import PepperPyError
from .module import BaseModule, ModuleMetadata

__all__ = [
    "PepperPyError",
    "BaseModule",
    "ModuleMetadata",
]
