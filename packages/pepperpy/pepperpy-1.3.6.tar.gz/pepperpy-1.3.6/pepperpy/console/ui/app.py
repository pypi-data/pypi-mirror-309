"""UI Application"""


from ..base import ConsoleApp
from .config import UIConfig
from .screen import Screen


class UIApp(ConsoleApp):
    """Rich UI application implementation"""
    
    def __init__(self, config: UIConfig | None = None):
        super().__init__(config or UIConfig())
        self.screen = Screen()
        self._components = {}
        
    async def initialize(self) -> None:
        """Initialize UI application"""
        await super().initialize()
        await self.screen.initialize()
        for component in self._components.values():
            await component.initialize()
            
    async def run(self) -> None:
        """Run UI application"""
        try:
            while True:
                await self.render()
                await self.handle_input()
        except Exception:
            await self.cleanup()
            
    async def cleanup(self) -> None:
        """Cleanup UI resources"""
        for component in self._components.values():
            await component.cleanup()
        await self.screen.cleanup()
        await super().cleanup() 