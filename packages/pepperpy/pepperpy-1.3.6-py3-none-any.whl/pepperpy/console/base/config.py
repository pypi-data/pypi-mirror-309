"""Console configuration"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConsoleConfig:
    """Base console configuration"""
    theme: str = "default"
    refresh_rate: int = 1
    force_terminal: bool = False
    metadata: dict[str, Any] = field(default_factory=dict) 