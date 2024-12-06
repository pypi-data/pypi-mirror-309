"""Toast notification component"""

from dataclasses import dataclass
from typing import Any, Literal

from rich.panel import Panel as RichPanel
from rich.text import Text

from .base import Component

ToastType = Literal["info", "success", "warning", "error"]

@dataclass
class ToastConfig:
    """Toast configuration"""
    type_: ToastType = "info"
    duration: float = 3.0
    style: str | None = None
    border_style: str | None = None

class Toast(Component):
    """Toast notification component"""
    
    def __init__(self, message: str, config: ToastConfig | None = None):
        super().__init__()
        self.message = message
        self.config = config or ToastConfig()
        
    def _get_style(self) -> tuple[str, str]:
        """Get toast style based on type"""
        styles = {
            "info": ("blue", "blue"),
            "success": ("green", "green"),
            "warning": ("yellow", "yellow"),
            "error": ("red", "red")
        }
        content_style, border = styles.get(self.config.type_, ("default", "default"))
        return (
            self.config.style or content_style,
            self.config.border_style or border
        )
        
    async def render(self) -> Any:
        """Render toast"""
        await super().render()
        
        content_style, border_style = self._get_style()
        text = Text(self.message, style=content_style)
        
        return RichPanel(
            text,
            border_style=border_style,
            padding=(0, 1)
        ) 