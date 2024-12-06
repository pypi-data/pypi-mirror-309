"""Markup file handler implementation"""

from pathlib import Path
from typing import Any

from lxml import etree

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class MarkupHandler(BaseHandler):
    """Handler for markup files (XML, HTML)"""

    async def read(self, path: Path) -> FileContent:
        """Read markup file"""
        try:
            metadata = await self._get_metadata(path)
            
            # Ler o arquivo como bytes
            with open(path, "rb") as f:
                content = f.read()

            # Parse XML/HTML
            tree = etree.fromstring(content)
            root = tree.getroottree()

            return FileContent(
                content=root,
                metadata=metadata.metadata,
                format=path.suffix.lstrip(".").lower(),
            )
        except Exception as e:
            raise FileError(f"Failed to read markup file: {e!s}", cause=e)

    async def write(
        self, path: Path, content: Any, metadata: dict[str, Any] | None = None
    ) -> FileMetadata:
        """Write markup file"""
        try:
            if isinstance(content, etree._Element):
                tree = content.getroottree()
                tree.write(
                    str(path),
                    encoding="utf-8",
                    xml_declaration=True,
                    pretty_print=True,
                )
            else:
                raise ValueError("Content must be an lxml Element")

            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write markup file: {e!s}", cause=e)
