"""Button component"""

from dataclasses import dataclass
from typing import Any, Callable

from rich.text import Text

from .base import Component


@dataclass
class ButtonConfig:
    """Button configuration"""
    label: str
    callback: Callable[[], None]
    style: str = "default"
    enabled: bool = True

class Button(Component):
    """Button component"""
    
    def __init__(self, config: ButtonConfig):
        super().__init__()
        self.config = config
        
    async def initialize(self) -> None:
        """Initialize button"""
        await super().initialize()
            
    async def render(self) -> Any:
        """Render button"""
        await super().render()
        
        style = self.config.style
        if not self.config.enabled:
            style = "dim " + style
            
        return Text(self.config.label, style=style)
        
    async def click(self) -> None:
        """Handle button click"""
        if self.config.enabled:
            self.config.callback()
            
    async def cleanup(self) -> None:
        """Cleanup button resources"""
        await super().cleanup()