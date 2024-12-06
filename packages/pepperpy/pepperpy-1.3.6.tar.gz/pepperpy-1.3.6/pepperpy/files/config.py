"""File handling configuration"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.config import ModuleConfig


@dataclass
class FileConfig(ModuleConfig):
    """Configuration for file operations"""

    default_encoding: str = "utf-8"
    chunk_size: int = 8192
    max_file_size: int | None = None
    allowed_extensions: set[str] | None = None
    create_dirs: bool = True
    backup_enabled: bool = False
    backup_dir: str | None = None
    metadata_enabled: bool = True
    params: dict[str, Any] = field(default_factory=dict)
