"""Base file handler implementation"""

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

import aiofiles
import magic

from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class BaseHandler(ABC):
    """Base class for file handlers"""

    async def _get_metadata(self, path: Path) -> FileMetadata:
        """Get file metadata"""
        try:
            stat = path.stat()
            mime = magic.Magic(mime=True)

            return FileMetadata(
                path=path,
                size=stat.st_size,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                mime_type=mime.from_file(str(path)),
            )
        except Exception as e:
            raise FileError(f"Failed to get file metadata: {e!s}", cause=e)

    async def _read_file(self, path: Path) -> str:
        """Read file content"""
        try:
            async with aiofiles.open(path) as file:
                return await file.read()
        except Exception as e:
            raise FileError(f"Failed to read file: {e!s}", cause=e)

    async def _write_file(self, path: Path, content: str) -> FileMetadata:
        """Write file content"""
        try:
            # Create directory if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(path, "w") as file:
                await file.write(content)

            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write file: {e!s}", cause=e)

    @abstractmethod
    async def read(self, path: Path) -> FileContent:
        """Read file content"""

    @abstractmethod
    async def write(
        self, path: Path, content: Any, metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write file content"""
