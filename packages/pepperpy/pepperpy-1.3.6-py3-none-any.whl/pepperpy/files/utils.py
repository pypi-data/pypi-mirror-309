"""File handling utilities"""

import filecmp
import hashlib
import os
import shutil
import tempfile
from pathlib import Path

from .exceptions import FileError


async def safe_move(src: Path, dst: Path, backup: bool = True) -> None:
    """Safely move file with backup"""
    try:
        if backup and dst.exists():
            backup_path = dst.with_suffix(f"{dst.suffix}.bak")
            shutil.copy2(dst, backup_path)

        shutil.move(src, dst)

    except Exception as e:
        raise FileError(f"Failed to move file: {e!s}", cause=e)


async def find_duplicates(directory: Path, recursive: bool = True) -> list[set[Path]]:
    """Find duplicate files"""
    try:
        # First pass: Group by size
        size_groups = {}
        pattern = "**/*" if recursive else "*"

        for path in directory.glob(pattern):
            if path.is_file():
                size = path.stat().st_size
                if size > 0:  # Ignore empty files
                    size_groups.setdefault(size, []).append(path)

        # Second pass: Compare files with same size
        duplicates = []
        for paths in size_groups.values():
            if len(paths) < 2:
                continue

            # Compare files
            while paths:
                current = paths.pop()
                matches = {current}

                for other in paths[:]:
                    if filecmp.cmp(current, other, shallow=False):
                        matches.add(other)
                        paths.remove(other)

                if len(matches) > 1:
                    duplicates.append(matches)

        return duplicates

    except Exception as e:
        raise FileError(f"Failed to find duplicates: {e!s}", cause=e)


async def atomic_write(path: Path, content: bytes, mode: int = 0o644) -> None:
    """Write file atomically"""
    try:
        # Create temporary file
        tmp_fd, tmp_path = tempfile.mkstemp(
            prefix=f".{path.name}.", dir=str(path.parent),
        )

        try:
            # Write content
            with os.fdopen(tmp_fd, "wb") as f:
                f.write(content)

            # Set permissions
            os.chmod(tmp_path, mode)

            # Atomic rename
            os.rename(tmp_path, path)

        finally:
            # Cleanup if needed
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    except Exception as e:
        raise FileError(f"Atomic write failed: {e!s}", cause=e)


async def verify_checksum(
    path: Path, expected: str, algorithm: str = "sha256", chunk_size: int = 8192,
) -> bool:
    """Verify file checksum"""
    try:
        hasher = getattr(hashlib, algorithm)()

        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)

        return hasher.hexdigest() == expected

    except Exception as e:
        raise FileError(f"Checksum verification failed: {e!s}", cause=e)
