"""Logging-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class LoggingError(PepperPyError):
    """Base logging error"""


class LogHandlerError(LoggingError):
    """Log handler error"""


class LogFormatterError(LoggingError):
    """Log formatter error"""


class LogFilterError(LoggingError):
    """Log filter error"""
