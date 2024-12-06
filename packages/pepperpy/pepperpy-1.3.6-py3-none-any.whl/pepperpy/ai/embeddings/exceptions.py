"""Embedding exceptions"""

from ..exceptions import AIError


class EmbeddingError(AIError):
    """Base exception for embedding errors"""


class ConfigurationError(EmbeddingError):
    """Configuration error"""


class ProviderError(EmbeddingError):
    """Provider error"""


class CacheError(EmbeddingError):
    """Cache error"""
