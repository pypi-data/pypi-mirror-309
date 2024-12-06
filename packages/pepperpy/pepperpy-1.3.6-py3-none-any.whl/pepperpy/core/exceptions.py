"""Core exceptions"""



class PepperPyError(Exception):
    """Base exception for all PepperPy errors"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.__cause__ = cause if cause is not None else None


class ConfigError(PepperPyError):
    """Configuration error"""


class ModuleError(PepperPyError):
    """Module error"""


class ResourceError(PepperPyError):
    """Resource error"""


class ValidationError(PepperPyError):
    """Validation error"""
