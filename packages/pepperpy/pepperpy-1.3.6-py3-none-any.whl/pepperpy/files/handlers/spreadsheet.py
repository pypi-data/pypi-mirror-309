"""Spreadsheet file handler implementation"""

from pathlib import Path
from typing import Any

import pandas as pd

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class SpreadsheetHandler(BaseHandler):
    """Handler for spreadsheet files"""

    async def read(self, path: Path) -> FileContent:
        """Read spreadsheet file"""
        try:
            metadata = await self._get_metadata(path)
            df = pd.read_excel(path)

            return FileContent(content=df, metadata=metadata.metadata, format="spreadsheet")
        except Exception as e:
            raise FileError(f"Failed to read spreadsheet file: {e!s}", cause=e)

    async def write(
        self, path: Path, content: pd.DataFrame, metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write spreadsheet file"""
        try:
            content.to_excel(path, index=False)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write spreadsheet file: {e!s}", cause=e)
