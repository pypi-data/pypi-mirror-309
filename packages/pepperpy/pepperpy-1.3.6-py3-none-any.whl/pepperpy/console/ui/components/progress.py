"""Progress bar component"""

from dataclasses import dataclass
from typing import Any

from rich.progress import Progress as RichProgress

from .base import Component


@dataclass
class ProgressConfig:
    """Progress bar configuration"""
    total: int = 100
    description: str = ""
    style: str = "default"


class ProgressBar(Component):
    """Progress bar component"""
    
    def __init__(self, total: int = 100):
        super().__init__()
        self.config = ProgressConfig(total=total)
        self._progress = RichProgress()
        self._task = self._progress.add_task("", total=total)
        
    async def initialize(self) -> None:
        """Initialize progress bar"""
        await super().initialize()
        
    async def cleanup(self) -> None:
        """Cleanup progress bar resources"""
        await super().cleanup()
        
    def set_progress(self, value: int, description: str | None = None) -> None:
        """Update progress value and description"""
        if description:
            self._progress.update(self._task, description=description)
        self._progress.update(self._task, completed=value)
        
    async def render(self) -> Any:
        """Render progress bar"""
        await super().render()
        return self._progress
