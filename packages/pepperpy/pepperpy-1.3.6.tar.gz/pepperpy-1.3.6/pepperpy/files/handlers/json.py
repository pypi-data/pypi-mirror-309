"""JSON file handler implementation"""

from pathlib import Path
from typing import Any

import orjson

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class JSONHandler(BaseHandler):
    """Handler for JSON files"""

    async def read(self, path: Path) -> FileContent:
        """Read JSON file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse JSON content
            data = orjson.loads(content)

            return FileContent(content=data, metadata=metadata.metadata, format="json")
        except Exception as e:
            raise FileError(f"Failed to read JSON file: {e!s}", cause=e)

    async def write(
        self,
        path: Path,
        content: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write JSON file"""
        try:
            # Convert to JSON
            json_content = orjson.dumps(
                content,
                option=orjson.OPT_INDENT_2 | orjson.OPT_SERIALIZE_NUMPY,
            ).decode("utf-8")

            return await self._write_file(path, json_content)
        except Exception as e:
            raise FileError(f"Failed to write JSON file: {e!s}", cause=e)
