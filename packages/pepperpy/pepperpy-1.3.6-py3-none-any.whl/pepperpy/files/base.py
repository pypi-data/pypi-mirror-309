"""Base file handler implementation"""

import hashlib
from collections.abc import AsyncIterator
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import aiofiles
import magic
from charset_normalizer import detect

from .exceptions import FileError
from .types import FileContent, FileMetadata


@runtime_checkable
class FileHandler(Protocol):
    """Protocol for file handlers"""

    async def read(self, path: Path) -> FileContent:
        """Read file content"""
        ...

    async def write(
        self, path: Path, content: Any, metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write file content"""
        ...


class BaseHandler:
    """Base file handler implementation"""

    async def _get_metadata(self, path: Path) -> FileMetadata:
        """Get file metadata"""
        try:
            stat = path.stat()
            file_type = magic.from_file(str(path), mime=True)
            encoding = None

            if not self._is_binary(path):
                async with aiofiles.open(path, "rb") as f:
                    content = await f.read()
                    encoding = detect(content)["encoding"]

            return FileMetadata(
                path=path,
                size=stat.st_size,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                mime_type=file_type,
                encoding=encoding,
                metadata=self._get_file_stats(path),
            )
        except Exception as e:
            raise FileError(f"Failed to get metadata: {e!s}", cause=e)

    def _get_file_stats(self, path: Path) -> dict[str, Any]:
        """Get detailed file statistics"""
        try:
            stat = path.stat()
            return {
                "name": path.name,
                "extension": path.suffix,
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime),
                "modified_at": datetime.fromtimestamp(stat.st_mtime),
                "hash": self._calculate_hash(path),
                "is_binary": self._is_binary(path),
                "permissions": oct(stat.st_mode)[-3:],
            }
        except Exception as e:
            raise FileError(f"Failed to get file stats: {e!s}", cause=e)

    def _is_binary(self, path: Path) -> bool:
        """Check if file is binary"""
        mime = magic.from_file(str(path), mime=True)
        return not mime.startswith(("text/", "application/json", "application/xml"))

    def _calculate_hash(self, path: Path) -> str:
        """Calculate file hash"""
        hasher = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    async def _read_file(self, path: Path) -> str:
        """Read file content as string"""
        try:
            if self._is_binary(path):
                raise FileError("Cannot read binary file as text")

            async with aiofiles.open(path) as f:
                return await f.read()
        except Exception as e:
            raise FileError(f"Failed to read file: {e!s}", cause=e)

    async def _write_file(self, path: Path, content: str) -> FileMetadata:
        """Write file content"""
        try:
            async with aiofiles.open(path, "w") as f:
                await f.write(content)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write file: {e!s}", cause=e)

    async def _read_chunks(self, path: Path, chunk_size: int = 8192) -> AsyncIterator[bytes]:
        """Read file in chunks"""
        try:
            async with aiofiles.open(path, "rb") as f:
                while chunk := await f.read(chunk_size):
                    yield chunk
        except Exception as e:
            raise FileError(f"Failed to read chunks: {e!s}", cause=e)

    async def _write_chunks(self, path: Path, chunks: AsyncIterator[bytes]) -> FileMetadata:
        """Write file in chunks"""
        try:
            async with aiofiles.open(path, "wb") as f:
                async for chunk in chunks:
                    await f.write(chunk)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write chunks: {e!s}", cause=e)
