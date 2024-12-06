"""File handling types"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Literal,
    Protocol,
    runtime_checkable,
)


@runtime_checkable
class PDFDocument(Protocol):
    """Protocol for PDF document"""

    metadata: dict[str, str]

    def get_toc(self) -> list[Any]: ...
    def get_form_text_fields(self) -> dict[str, str]: ...
    def new_page(self) -> "PDFPage": ...
    def set_metadata(self, metadata: dict[str, Any]) -> None: ...
    def save(self, path: str, **kwargs: Any) -> None: ...
    def close(self) -> None: ...
    def extract_image(self, xref: int) -> dict[str, Any]: ...
    def __iter__(self) -> Any: ...


@runtime_checkable
class PDFPage(Protocol):
    """Protocol for PDF page"""

    parent: PDFDocument

    def get_text(self) -> str: ...
    def get_links(self) -> list[dict[str, Any]]: ...
    def get_images(self) -> list[Any]: ...
    def insert_text(self, point: tuple[float, float], text: str) -> None: ...
    def insert_image(self, rect: Any, stream: bytes) -> None: ...


@dataclass
class MediaInfo:
    type: Literal["image", "video", "audio"]
    width: int | None = None
    height: int | None = None
    format: str | None = None
    mode: str | None = None
    channels: int | None = None
    duration: float | None = None
    fps: float | None = None
    total_frames: int | None = None
    sample_width: int | None = None
    frame_rate: int | None = None


@dataclass
class FileContent:
    content: Any
    metadata: dict[str, Any]
    format: str


@dataclass
class SpreadsheetStats:
    row_count: int
    column_count: int
    missing_values: dict[str, int]
    column_types: dict[str, Any]
    numeric_stats: dict[str, dict[str, float]]
    memory_usage: int
    duplicates: int


@dataclass
class FileMetadata:
    """File metadata"""

    path: Path
    size: int
    created_at: datetime
    modified_at: datetime
    mime_type: str | None = None
    encoding: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chapter:
    """E-book chapter"""

    title: str
    content: str
    order: int
    level: int = 1
    identifier: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubTOC:
    """E-book table of contents"""

    items: list[Chapter]
    max_depth: int = 3


@dataclass
class ImageInfo:
    """Image information"""

    width: int
    height: int
    mode: str
    format: str
    channels: int | None = None
    bits: int | None = None
    dpi: tuple[float, float] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioInfo:
    """Audio file information"""

    duration: float
    sample_rate: int
    channels: int
    format: str
    bit_depth: int | None = None
    bitrate: int | None = None
    codec: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileStats:
    """File statistics"""

    name: str
    extension: str
    size: int
    created_at: datetime
    modified_at: datetime
    hash: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubAsset:
    """Base class for EPUB assets (images, audio, etc)"""

    identifier: str
    media_type: str
    content: bytes
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubImage(EpubAsset):
    """Image asset in EPUB"""

    width: int | None = None
    height: int | None = None
    format: str | None = None


@dataclass
class EpubLink:
    """Link in EPUB content"""

    text: str
    href: str
    type: Literal["internal", "external", "resource"]
    target: str | None = None


@dataclass
class EpubChapterContent:
    """Structured content of an EPUB chapter"""

    html: str
    text: str
    images: list[EpubImage]
    links: list[EpubLink]
    tables: list[str]
    headers: list[tuple[int, str]]  # level, text
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubChapter:
    """Enhanced EPUB chapter with structured content"""

    title: str
    content: EpubChapterContent
    order: int
    level: int = 1
    identifier: str | None = None
    file_name: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubStructure:
    """Complete EPUB book structure"""

    metadata: dict[str, Any]
    chapters: list[EpubChapter]
    assets: list[EpubAsset]
    toc: EpubTOC
