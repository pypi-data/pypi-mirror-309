"""Configuration-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class ConfigError(PepperPyError):
    """Base configuration error"""


class ConfigLoadError(ConfigError):
    """Configuration loading error"""


class ConfigValidationError(ConfigError):
    """Configuration validation error"""


class ConfigParseError(ConfigError):
    """Configuration parsing error"""
