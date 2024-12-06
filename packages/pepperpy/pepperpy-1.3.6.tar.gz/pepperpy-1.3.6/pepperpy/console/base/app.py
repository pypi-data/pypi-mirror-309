"""Base console application"""

from abc import ABC, abstractmethod
from typing import Any

from .config import ConsoleConfig
from .console import Console


class ConsoleApp(ABC):
    """Base console application"""
    
    def __init__(self, config: ConsoleConfig | None = None):
        self.config = config or ConsoleConfig()
        self.console = Console(self.config)
        self._initialized = False
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize application"""
        self._initialized = True
        
    @abstractmethod
    async def render(self) -> Any:
        """Render application"""
        if not self._initialized:
            await self.initialize()
            
    @abstractmethod
    async def handle_input(self) -> None:
        """Handle user input"""
        pass
        
    @abstractmethod
    async def run(self) -> None:
        """Run application"""
        try:
            await self.initialize()
            while True:
                await self.render()
                await self.handle_input()
        except Exception:
            await self.cleanup()
            raise
            
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup application resources"""
        self.console.clear()
        self._initialized = False