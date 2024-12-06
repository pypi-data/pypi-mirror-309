"""Plugin-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class PluginError(PepperPyError):
    """Base plugin error"""


class PluginLoadError(PluginError):
    """Plugin loading error"""


class PluginNotFoundError(PluginError):
    """Plugin not found error"""


class PluginConfigError(PluginError):
    """Plugin configuration error"""
