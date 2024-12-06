"""Database configuration"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DatabaseConfig:
    """Database configuration"""

    engine: str
    database: str
    host: str | None = None
    port: int | None = None
    user: str | None = None
    password: str | None = None
    pool_size: int = 10
    timeout: float = 30.0
    params: dict[str, Any] = field(default_factory=dict)
