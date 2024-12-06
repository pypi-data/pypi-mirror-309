"""Text chunking implementation"""

import re
from re import Pattern

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import TextConfig
from .exceptions import TextProcessingError
from .types import ChunkMetadata, TextChunk


class TextChunker(BaseModule):
    """Smart text chunking with various strategies"""

    # Common sentence boundary patterns
    SENTENCE_BOUNDARIES: Pattern = re.compile(r"(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\s*$")

    def __init__(self, config: TextConfig | None = None):
        super().__init__()
        self.metadata = ModuleMetadata(
            name="text_chunker",
            version="1.0.0",
            description="Text chunking functionality",
            dependencies=[],
            config=config.dict() if config else {},
        )
        self._tokenizer = None

    async def _setup(self) -> None:
        """Initialize chunker"""
        if self.config.get("use_tokenizer"):
            try:
                from transformers import AutoTokenizer

                self._tokenizer = AutoTokenizer.from_pretrained(
                    self.config.get("tokenizer_model", "gpt2"),
                )
            except ImportError:
                raise TextProcessingError(
                    "Tokenizer requested but transformers not installed. "
                    "Install with: pip install transformers",
                )
            except Exception as e:
                raise TextProcessingError("Failed to initialize tokenizer", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        self._tokenizer = None

    async def chunk_text(self, text: str) -> list[TextChunk]:
        """Split text into chunks with metadata"""
        if not text:
            return []

        try:
            chunks = []
            current_pos = 0
            text_length = len(text)

            while current_pos < text_length:
                # Find next chunk boundary
                chunk_end = self._find_chunk_boundary(
                    text, current_pos, self.config.get("max_chunk_size", 1000),
                )

                # Extract chunk content
                chunk_content = text[current_pos:chunk_end].strip()
                if not chunk_content:
                    current_pos = chunk_end
                    continue

                # Create chunk with metadata
                chunk = TextChunk(
                    content=chunk_content,
                    metadata=ChunkMetadata(
                        start_index=current_pos,
                        end_index=chunk_end,
                        tokens=self._count_tokens(chunk_content),
                    ),
                )
                chunks.append(chunk)

                # Move position considering overlap
                overlap = self.config.get("overlap", 100)
                current_pos = max(
                    current_pos + 1,
                    chunk_end - (overlap if overlap < chunk_end - current_pos else 0),
                )

            return chunks

        except Exception as e:
            raise TextProcessingError(f"Chunking failed: {e!s}", cause=e)

    def _find_chunk_boundary(self, text: str, start: int, max_size: int) -> int:
        """Find appropriate chunk boundary"""
        if start + max_size >= len(text):
            return len(text)

        # Try to break at sentence boundary
        if self.config.get("respect_sentences", True):
            for match in self.SENTENCE_BOUNDARIES.finditer(text[start : start + max_size + 50]):
                end = start + match.end()
                if end - start >= self.config.get("min_chunk_size", 100):
                    return end

        # Fall back to word boundary
        pos = start + max_size
        while pos > start and not text[pos].isspace():
            pos -= 1

        return pos if pos > start else start + max_size

    def _count_tokens(self, text: str) -> int | None:
        """Count tokens if tokenizer is available"""
        if self._tokenizer:
            return len(self._tokenizer.encode(text))
        return None
