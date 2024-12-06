"""File compression and optimization handler"""

import bz2
import gzip
import io
import lzma
import zlib
from pathlib import Path
from typing import Any

from ..exceptions import FileError
from .base import BaseHandler


class CompressionHandler(BaseHandler):
    """Handler for file compression"""

    COMPRESSION_LEVELS = {"fast": 1, "balanced": 6, "max": 9}

    async def compress_gzip(
        self, data: bytes, level: str = "balanced", filename: str | None = None,
    ) -> bytes:
        """Compress data using gzip"""
        try:
            compression_level = self.COMPRESSION_LEVELS[level]
            out = io.BytesIO()

            with gzip.GzipFile(
                filename=filename, mode="wb", compresslevel=compression_level, fileobj=out,
            ) as gz:
                gz.write(data)

            return out.getvalue()

        except Exception as e:
            raise FileError(f"Gzip compression failed: {e!s}", cause=e)

    async def decompress_gzip(self, data: bytes) -> bytes:
        """Decompress gzip data"""
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(data), mode="rb") as gz:
                return gz.read()
        except Exception as e:
            raise FileError(f"Gzip decompression failed: {e!s}", cause=e)

    async def compress_bzip2(self, data: bytes, level: str = "balanced") -> bytes:
        """Compress data using bzip2"""
        try:
            compression_level = self.COMPRESSION_LEVELS[level]
            return bz2.compress(data, compresslevel=compression_level)
        except Exception as e:
            raise FileError(f"Bzip2 compression failed: {e!s}", cause=e)

    async def decompress_bzip2(self, data: bytes) -> bytes:
        """Decompress bzip2 data"""
        try:
            return bz2.decompress(data)
        except Exception as e:
            raise FileError(f"Bzip2 decompression failed: {e!s}", cause=e)

    async def compress_lzma(
        self, data: bytes, level: str = "balanced", format: int | None = None,
    ) -> bytes:
        """Compress data using LZMA"""
        try:
            compression_level = self.COMPRESSION_LEVELS[level]
            filters = [{"id": lzma.FILTER_LZMA2, "preset": compression_level}]

            return lzma.compress(data, format=format or lzma.FORMAT_XZ, filters=filters)
        except Exception as e:
            raise FileError(f"LZMA compression failed: {e!s}", cause=e)

    async def decompress_lzma(self, data: bytes) -> bytes:
        """Decompress LZMA data"""
        try:
            return lzma.decompress(data)
        except Exception as e:
            raise FileError(f"LZMA decompression failed: {e!s}", cause=e)

    async def compress_zlib(self, data: bytes, level: str = "balanced") -> bytes:
        """Compress data using zlib"""
        try:
            compression_level = self.COMPRESSION_LEVELS[level]
            return zlib.compress(data, level=compression_level)
        except Exception as e:
            raise FileError(f"Zlib compression failed: {e!s}", cause=e)

    async def decompress_zlib(self, data: bytes) -> bytes:
        """Decompress zlib data"""
        try:
            return zlib.decompress(data)
        except Exception as e:
            raise FileError(f"Zlib decompression failed: {e!s}", cause=e)

    async def compress_file(
        self,
        input_path: Path,
        output_path: Path | None = None,
        method: str = "gzip",
        level: str = "balanced",
        chunk_size: int = 8192,
    ) -> Path:
        """Compress file using specified method"""
        try:
            if output_path is None:
                output_path = input_path.with_suffix(f"{input_path.suffix}.{method}")

            compression_funcs = {
                "gzip": self.compress_gzip,
                "bzip2": self.compress_bzip2,
                "lzma": self.compress_lzma,
                "zlib": self.compress_zlib,
            }

            if method not in compression_funcs:
                raise FileError(f"Unsupported compression method: {method}")

            compress = compression_funcs[method]

            # Process file in chunks
            with open(input_path, "rb") as f_in:
                data = f_in.read()
                compressed = await compress(data, level=level)

                with open(output_path, "wb") as f_out:
                    f_out.write(compressed)

            return output_path

        except Exception as e:
            raise FileError(f"File compression failed: {e!s}", cause=e)

    async def decompress_file(
        self, input_path: Path, output_path: Path | None = None, method: str = "auto",
    ) -> Path:
        """Decompress file using specified or auto-detected method"""
        try:
            if output_path is None:
                # Remove compression extension
                stem = input_path.stem
                if stem.endswith((".gz", ".bz2", ".xz", ".zlib")):
                    stem = stem.rsplit(".", 1)[0]
                output_path = input_path.with_name(stem)

            # Auto-detect method from extension
            if method == "auto":
                suffix = input_path.suffix.lower()
                method = {".gz": "gzip", ".bz2": "bzip2", ".xz": "lzma", ".zlib": "zlib"}.get(
                    suffix, "gzip",
                )

            decompression_funcs = {
                "gzip": self.decompress_gzip,
                "bzip2": self.decompress_bzip2,
                "lzma": self.decompress_lzma,
                "zlib": self.decompress_zlib,
            }

            if method not in decompression_funcs:
                raise FileError(f"Unsupported decompression method: {method}")

            decompress = decompression_funcs[method]

            # Process file
            with open(input_path, "rb") as f_in:
                data = f_in.read()
                decompressed = await decompress(data)

                with open(output_path, "wb") as f_out:
                    f_out.write(decompressed)

            return output_path

        except Exception as e:
            raise FileError(f"File decompression failed: {e!s}", cause=e)

    async def get_compression_info(self, path: Path) -> dict[str, Any]:
        """Get compression information about file"""
        try:
            original_size = path.stat().st_size
            info = {
                "original_size": original_size,
                "compressed_size": original_size,
                "ratio": 1.0,
                "method": "none",
            }

            # Try to detect compression method
            with open(path, "rb") as f:
                magic = f.read(4)

                if magic.startswith(b"\x1f\x8b"):
                    info["method"] = "gzip"
                elif magic.startswith(b"BZh"):
                    info["method"] = "bzip2"
                elif magic.startswith(b"\xfd7zXZ"):
                    info["method"] = "lzma"
                elif magic.startswith(b"x\x9c"):
                    info["method"] = "zlib"

            # If compressed, get original size
            if info["method"] != "none":
                decompressed = await self.decompress_file(path)
                info["original_size"] = decompressed.stat().st_size
                info["compressed_size"] = original_size
                info["ratio"] = original_size / info["original_size"]

            return info

        except Exception as e:
            raise FileError(f"Failed to get compression info: {e!s}", cause=e)
