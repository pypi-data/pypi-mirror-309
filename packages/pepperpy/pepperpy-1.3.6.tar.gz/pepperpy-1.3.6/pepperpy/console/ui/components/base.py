"""Base component functionality"""

from abc import ABC, abstractmethod
from typing import Any

from ..styles import Style


class Component(ABC):
    """Base UI component"""
    
    def __init__(self):
        self.style = Style()
        self._initialized = False
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize component"""
        self._initialized = True
        
    @abstractmethod
    async def render(self) -> Any:
        """Render component"""
        if not self._initialized:
            await self.initialize()
            
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup component resources"""
        self._initialized = False 