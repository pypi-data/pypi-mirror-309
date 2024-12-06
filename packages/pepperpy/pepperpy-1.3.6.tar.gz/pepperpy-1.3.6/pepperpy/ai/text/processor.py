"""Text processing implementation"""

import re
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import TextConfig
from .exceptions import TextProcessingError


class TextProcessor(BaseModule):
    """Text processing and manipulation"""

    def __init__(self, config: TextConfig | None = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="text_processor",
            version="1.0.0",
            description="Text processing functionality",
            dependencies=[],
            config=vars(config) if config else {},
        )

    async def _setup(self) -> None:
        """Initialize processor"""

    async def _cleanup(self) -> None:
        """Cleanup resources"""

    async def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        try:
            # Remove excessive whitespace
            if not self.config.get("preserve_whitespace", False):
                text = " ".join(text.split())

            # Normalize quotes
            text = re.sub(r'[""]', '"', text)
            text = re.sub(r"[" "]", "'", text)

            # Normalize dashes
            text = re.sub(r"[–—]", "-", text)

            # Normalize ellipsis
            text = re.sub(r"\.{3,}", "...", text)

            return text.strip()

        except Exception as e:
            raise TextProcessingError(f"Text cleaning failed: {e!s}", cause=e)

    async def extract_metadata(self, text: str) -> dict[str, Any]:
        """Extract metadata from text"""
        metadata = {}

        try:
            # Extract URLs
            urls = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                text,
            )
            if urls:
                metadata["urls"] = urls

            # Extract email addresses
            emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", text)
            if emails:
                metadata["emails"] = emails

            # Extract hashtags
            hashtags = re.findall(r"#\w+", text)
            if hashtags:
                metadata["hashtags"] = hashtags

            # Extract mentions
            mentions = re.findall(r"@\w+", text)
            if mentions:
                metadata["mentions"] = mentions

            # Basic language detection
            if len(text.split()) > 3:  # Only try if we have enough text
                try:
                    from langdetect import detect

                    metadata["language"] = detect(text)
                except ImportError:
                    pass  # Language detection optional

            return metadata

        except Exception as e:
            raise TextProcessingError(f"Metadata extraction failed: {e!s}", cause=e)

    async def format_text(self, text: str, width: int | None = None, indent: int = 0) -> str:
        """Format text with wrapping and indentation"""
        try:
            if not width:
                return text

            lines = []
            current_line = []
            current_width = 0

            for word in text.split():
                word_width = len(word)

                if current_width + word_width + 1 > width:
                    if current_line:
                        lines.append(" " * indent + " ".join(current_line))
                        current_line = []
                        current_width = 0

                current_line.append(word)
                current_width += word_width + 1

            if current_line:
                lines.append(" " * indent + " ".join(current_line))

            return "\n".join(lines)

        except Exception as e:
            raise TextProcessingError(f"Text formatting failed: {e!s}", cause=e)
