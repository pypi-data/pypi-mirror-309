"""Image file handler implementation"""

from pathlib import Path
from typing import Any

from PIL import Image, ImageOps
from PIL.Image import Resampling

from ..exceptions import FileError
from ..types import FileContent, FileMetadata, ImageInfo
from .base import BaseHandler


class ImageHandler(BaseHandler):
    """Handler for image files"""

    async def read(self, path: Path) -> FileContent:
        """Read image file"""
        try:
            metadata = await self._get_metadata(path)
            with Image.open(path) as img:
                # Extract image info and convert complex keys to strings
                img_info = {str(k): v for k, v in img.info.items()}

                info = ImageInfo(
                    width=img.width,
                    height=img.height,
                    mode=img.mode,
                    format=img.format or "",
                    channels=len(img.getbands()),
                    bits=8,  # Default to 8 bits per channel
                    dpi=img.info.get("dpi"),
                    metadata=img_info,  # Now using the converted dictionary
                )

                enhanced_metadata = {
                    **metadata.metadata,
                    "info": info,
                }

                return FileContent(content=img.copy(), metadata=enhanced_metadata, format="image")
        except Exception as e:
            raise FileError(f"Failed to read image file: {e!s}", cause=e)

    async def write(
        self,
        path: Path,
        content: Image.Image,
        metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write image file"""
        try:
            content.save(path)
            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write image file: {e!s}", cause=e)

    def resize(
        self, image: Image.Image, size: tuple[int, int], keep_aspect: bool = True,
    ) -> Image.Image:
        """Resize image"""
        if keep_aspect:
            return ImageOps.contain(image, size, Resampling.LANCZOS)
        return image.resize(size, Resampling.LANCZOS)

    def create_thumbnail(self, image: Image.Image, size: tuple[int, int]) -> Image.Image:
        """Create image thumbnail"""
        thumb = image.copy()
        thumb.thumbnail(size, Resampling.LANCZOS)
        return thumb
