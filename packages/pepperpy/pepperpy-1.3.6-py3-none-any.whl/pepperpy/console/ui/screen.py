"""Screen management for UI applications"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from rich.console import Console
from rich.live import Live
from rich.text import Text


class Direction(Enum):
    """Scroll direction"""

    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class ScreenConfig:
    """Screen configuration"""

    width: int | None = None
    height: int | None = None
    refresh_per_second: int = 30
    auto_refresh: bool = True


class Screen:
    """Screen management for UI applications"""

    def __init__(self, config: ScreenConfig | None = None):
        self.config = config or ScreenConfig()
        self._console = Console(width=self.config.width, height=self.config.height)
        self._live = Live(
            console=self._console,
            refresh_per_second=self.config.refresh_per_second,
            auto_refresh=self.config.auto_refresh,
        )
        self._content: Any = None

    async def initialize(self) -> None:
        """Initialize screen"""
        self._live.start()

    def update(self, content: Any) -> None:
        """Update screen content"""
        self._content = content
        self._live.update(content)

    def scroll(self, direction: Direction, lines: int = 1) -> None:
        """Scroll screen content"""
        if not self._content:
            return

        if direction in (Direction.UP, Direction.DOWN):
            self._scroll_vertical(direction, lines)
        else:
            self._scroll_horizontal(direction, lines)

    def _scroll_vertical(self, direction: Direction, lines: int) -> None:
        """Scroll content vertically"""
        if isinstance(self._content, Text):
            # Convert Text to str for manipulation
            content_str = str(self._content)
            text_lines = content_str.split("\n")

            if direction == Direction.UP:
                text_lines = text_lines[lines:] + text_lines[:lines]
            else:
                text_lines = text_lines[-lines:] + text_lines[:-lines]

            # Create new Text from joined lines
            self._content = Text("\n".join(text_lines))
            self._live.update(self._content)

    def _scroll_horizontal(self, direction: Direction, lines: int) -> None:
        """Scroll content horizontally"""
        if isinstance(self._content, Text):
            content_str = str(self._content)

            if direction == Direction.LEFT:
                new_content = content_str[lines:]
            else:
                new_content = " " * lines + content_str

            self._content = Text(new_content)
            self._live.update(self._content)

    async def cleanup(self) -> None:
        """Cleanup screen"""
        self._live.stop()
        self._console.clear()
