"""Rich console application"""

from typing import Any

from ..base import ConsoleApp
from .config import RichConfig


class RichConsoleApp(ConsoleApp):
    """Rich console application implementation"""
    
    def __init__(self, config: RichConfig | None = None):
        super().__init__(config or RichConfig())
        self._content: Any = None
        
    async def initialize(self) -> None:
        """Initialize rich console application"""
        await super().initialize()
        
    async def render(self) -> None:
        """Render content"""
        await super().render()
        if self._content is not None:
            self.console.print(self._content)
            
    async def handle_input(self) -> None:
        """Handle user input"""
        pass
        
    def set_content(self, content: Any) -> None:
        """Set content to render"""
        self._content = content
