"""Metrics type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from pepperpy.core.types import JsonDict


class MetricType(Enum):
    """Types of metrics"""

    LATENCY = "latency"
    TOKEN_COUNT = "token_count"  # noqa: S105
    PROMPT_LENGTH = "prompt_length"
    RESPONSE_LENGTH = "response_length"
    CACHE_HIT = "cache_hit"
    ERROR = "error"
    CUSTOM = "custom"


@dataclass
class MetricEvent:
    """Metric event data"""

    type: MetricType
    value: Any
    module: str
    operation: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: JsonDict = field(default_factory=dict)
