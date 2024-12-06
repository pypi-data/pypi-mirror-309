"""UI styling system"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Style:
    """Component style configuration"""
    color: str = "default"
    background: str = "default"
    bold: bool = False
    italic: bool = False
    underline: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass
class Theme:
    """UI theme configuration"""
    name: str
    styles: dict[str, Style] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_style(self, component: str) -> Style:
        """Get style for component"""
        return self.styles.get(component, Style()) 