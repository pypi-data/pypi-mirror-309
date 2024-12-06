"""LLM exceptions"""


class LLMError(Exception):
    """Base exception for LLM errors"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class ProviderError(LLMError):
    """Exception raised by LLM providers"""



class ConfigurationError(LLMError):
    """Error in LLM configuration"""


class GenerationError(LLMError):
    """Error during text generation"""
