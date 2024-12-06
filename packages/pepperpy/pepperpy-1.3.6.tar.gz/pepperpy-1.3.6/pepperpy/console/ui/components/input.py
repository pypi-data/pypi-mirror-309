"""Input component for text entry"""

from dataclasses import dataclass
from typing import Any, Callable

from rich.text import Text

from .base import Component


@dataclass
class InputConfig:
    """Input configuration"""
    placeholder: str = ""
    password: bool = False
    max_length: int | None = None
    validator: Callable[[str], bool] | None = None
    formatter: Callable[[str], str] | None = None
    style: str = "default"
    error_style: str = "red"

class Input(Component):
    """Input component for text entry"""
    
    def __init__(self, config: InputConfig | None = None):
        super().__init__()
        self.config = config or InputConfig()
        self._value: str = ""
        self._focused: bool = False
        self._error: str | None = None
        
    @property
    def value(self) -> str:
        """Get current input value"""
        return self._value
        
    @value.setter
    def value(self, new_value: str) -> None:
        """Set input value with validation and formatting"""
        if self.config.max_length and len(new_value) > self.config.max_length:
            self._error = f"Value exceeds maximum length of {self.config.max_length}"
            return
            
        if self.config.validator and not self.config.validator(new_value):
            self._error = "Invalid value"
            return
            
        self._value = (self.config.formatter(new_value) 
                      if self.config.formatter 
                      else new_value)
        self._error = None
        
    def focus(self) -> None:
        """Focus input"""
        self._focused = True
        
    def blur(self) -> None:
        """Blur input"""
        self._focused = False
        
    async def render(self) -> Any:
        """Render input"""
        await super().render()
        
        text = Text()
        
        # Add placeholder if empty
        if not self._value and self.config.placeholder:
            text.append(self.config.placeholder, style="dim")
            return text
            
        # Render value (mask if password)
        display_value = "*" * len(self._value) if self.config.password else self._value
        text.append(display_value, style=self.config.style)
        
        # Add cursor if focused
        if self._focused:
            text.append("_", style="blink")
            
        # Add error if any
        if self._error:
            text.append(f"\n{self._error}", style=self.config.error_style)
            
        return text 