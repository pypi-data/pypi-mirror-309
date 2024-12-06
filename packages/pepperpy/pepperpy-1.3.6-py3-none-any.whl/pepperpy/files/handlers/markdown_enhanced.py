"""Enhanced Markdown file handler implementation"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from markdown_it import MarkdownIt
from markdown_it.token import Token

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


@dataclass
class Section:
    """Markdown document section"""

    title: str
    level: int
    content: str
    start: int
    end: int


@dataclass
class TableOfContents:
    """Markdown document table of contents"""

    sections: list[Section]
    max_depth: int = 3


@dataclass
class MarkdownOptions:
    """Markdown parser options"""

    max_depth: int = 3
    include_titles: bool = True
    include_sections: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class MarkdownEnhancedHandler(BaseHandler):
    """Enhanced handler for Markdown files with TOC and section support"""

    def __init__(self):
        super().__init__()
        self._parser = MarkdownIt("commonmark", {"html": True})
        self._options = MarkdownOptions()

    async def read(self, path: Path) -> FileContent:
        """Read Markdown file with enhanced features"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse content and extract sections
            tokens = self._parser.parse(content)
            sections = self._extract_sections(tokens)
            toc = self._generate_toc(sections)

            # Generate final content
            enhanced_metadata = {
                **metadata.metadata,
                "toc": toc,
                "sections": sections,
            }

            return FileContent(
                content=content, metadata=enhanced_metadata, format="markdown_enhanced",
            )
        except Exception as e:
            raise FileError(f"Failed to read enhanced Markdown file: {e!s}", cause=e)

    async def write(
        self, path: Path, content: str, metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write Markdown file"""
        try:
            return await self._write_file(path, content)
        except Exception as e:
            raise FileError(f"Failed to write enhanced Markdown file: {e!s}", cause=e)

    def _extract_sections(self, tokens: list[Token]) -> list[Section]:
        """Extract sections from Markdown tokens"""
        sections: list[Section] = []
        current_section: Section | None = None
        content_buffer: list[str] = []

        for token in tokens:
            if token.type == "heading_open":
                if current_section:
                    current_section.content = "".join(content_buffer)
                    sections.append(current_section)

                level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
                title_token = tokens[tokens.index(token) + 1]
                current_section = Section(
                    title=title_token.content,
                    level=level,
                    content="",
                    start=token.map[0] if token.map else 0,
                    end=0,
                )
                content_buffer = []
            elif token.type == "inline":
                content_buffer.append(token.content)

        if current_section:
            current_section.content = "".join(content_buffer)
            sections.append(current_section)

        return sections

    def _generate_toc(self, sections: list[Section]) -> TableOfContents:
        """Generate table of contents from sections"""
        max_depth = self._options.max_depth
        filtered_sections = [section for section in sections if section.level <= max_depth]
        return TableOfContents(sections=filtered_sections, max_depth=max_depth)
