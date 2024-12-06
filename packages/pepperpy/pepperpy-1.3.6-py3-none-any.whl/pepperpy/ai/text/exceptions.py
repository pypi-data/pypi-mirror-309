"""Text processing exceptions"""

from pepperpy.core.exceptions import PepperPyError


class TextProcessingError(PepperPyError):
    """Base exception for text processing errors"""


class ChunkingError(TextProcessingError):
    """Error during text chunking"""


class ProcessingError(TextProcessingError):
    """Error during text processing"""
