"""AI module exceptions"""

from pepperpy.core.exceptions import PepperPyError


class AIError(PepperPyError):
    """Base exception for AI errors"""


class ModelError(AIError):
    """Error during model operations"""


class ProcessingError(AIError):
    """Error during data processing"""


class ValidationError(AIError):
    """Error during data validation"""


class ConfigurationError(AIError):
    """Error in AI configuration"""
