"""AI metrics exceptions"""

from pepperpy.core.exceptions import PepperPyError


class MetricsError(PepperPyError):
    """Base exception for metrics errors"""


class CollectionError(MetricsError):
    """Error during metrics collection"""


class ValidationError(MetricsError):
    """Error during metrics validation"""


class ProcessingError(MetricsError):
    """Error during metrics processing"""
