"""YAML file handler implementation"""

from pathlib import Path
from typing import Any

import yaml

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class YAMLHandler(BaseHandler):
    """Handler for YAML files"""

    async def read(self, path: Path) -> FileContent:
        """Read YAML file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse YAML content
            data = yaml.safe_load(content)

            return FileContent(content=data, metadata=metadata.metadata, format="yaml")
        except Exception as e:
            raise FileError(f"Failed to read YAML file: {e!s}", cause=e)

    async def write(
        self, path: Path, content: dict[str, Any], metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write YAML file"""
        try:
            # Convert to YAML
            yaml_content = yaml.safe_dump(content, default_flow_style=False, allow_unicode=True)

            return await self._write_file(path, yaml_content)
        except Exception as e:
            raise FileError(f"Failed to write YAML file: {e!s}", cause=e)
