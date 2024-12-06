"""Text processing types"""

from dataclasses import dataclass, field
from datetime import datetime

from pepperpy.core.types import JsonDict


@dataclass
class ChunkMetadata:
    """Metadata for text chunks"""

    start_index: int
    end_index: int
    tokens: int | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TextChunk:
    """Chunk of processed text"""

    content: str
    metadata: ChunkMetadata
    created_at: datetime = field(default_factory=datetime.utcnow)
