"""File manager implementation"""


from .base import FileHandler
from .exceptions import FileError
from .handlers.audio import AudioHandler
from .handlers.config import ConfigFileHandler
from .handlers.epub import EPUBHandler
from .handlers.image import ImageHandler
from .handlers.json import JSONHandler
from .handlers.markdown import MarkdownHandler
from .handlers.markdown_enhanced import MarkdownEnhancedHandler
from .handlers.markup import MarkupHandler
from .handlers.pdf import PDFHandler
from .handlers.spreadsheet import SpreadsheetHandler
from .handlers.yaml import YAMLHandler


class FileManager:
    """File manager for handling different file types"""

    def __init__(self):
        self._handlers: dict[str, FileHandler] = {}
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """Register default file handlers"""
        self.register_handler("audio", AudioHandler())
        self.register_handler("config", ConfigFileHandler())
        self.register_handler("epub", EPUBHandler())
        self.register_handler("image", ImageHandler())
        self.register_handler("json", JSONHandler())
        self.register_handler("markdown", MarkdownHandler())
        self.register_handler("markdown_enhanced", MarkdownEnhancedHandler())
        self.register_handler("markup", MarkupHandler())
        self.register_handler("pdf", PDFHandler())
        self.register_handler("spreadsheet", SpreadsheetHandler())
        self.register_handler("yaml", YAMLHandler())

    def register_handler(self, name: str, handler: FileHandler) -> None:
        """
        Register file handler

        Args:
            name: Handler name
            handler: File handler instance

        """
        self._handlers[name] = handler

    def get_handler(self, name: str) -> FileHandler:
        """
        Get file handler by name

        Args:
            name: Handler name

        Returns:
            FileHandler: File handler instance

        Raises:
            FileError: If handler not found

        """
        if name not in self._handlers:
            raise FileError(f"Handler not found: {name}")
        return self._handlers[name]


# Global file manager instance
manager = FileManager()
