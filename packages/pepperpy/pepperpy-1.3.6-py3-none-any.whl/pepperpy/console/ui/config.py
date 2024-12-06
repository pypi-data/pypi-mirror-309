"""UI configuration"""

from dataclasses import dataclass, field
from typing import Any

from ..base.config import ConsoleConfig


@dataclass
class UIConfig(ConsoleConfig):
    """UI specific configuration"""
    screen_width: int = 120
    screen_height: int = 30
    animation_enabled: bool = True
    animation_fps: int = 30
    default_style: str = "default"
    default_theme: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict) 