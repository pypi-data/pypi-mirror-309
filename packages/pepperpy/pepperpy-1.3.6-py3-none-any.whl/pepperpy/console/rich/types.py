"""Rich type definitions"""

from dataclasses import dataclass

from rich.style import Style


@dataclass
class RichTheme:
    """Rich theme configuration"""

    styles: dict[str, Style]
    inherit: bool = True


@dataclass
class RichLayout:
    """Rich layout configuration"""

    name: str
    title: str | None = None
    minimum_size: int = 1
    ratio: int = 1
    visible: bool = True
