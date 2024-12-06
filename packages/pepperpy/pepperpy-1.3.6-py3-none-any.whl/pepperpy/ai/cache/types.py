"""Cache type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from pepperpy.core.types import JsonDict


@dataclass
class CacheEntry:
    """Cache entry data"""

    key: str
    value: Any
    expires_at: datetime | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class VectorEntry:
    """Vector cache entry"""

    key: str
    vector: Any
    metadata: JsonDict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
