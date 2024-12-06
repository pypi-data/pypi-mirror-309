"""Rich console implementation"""

from typing import Any, Literal

from rich.console import Console as RichConsoleBase

from ..base import Console
from .config import RichConfig

# Define os tipos válidos de color_system
ColorSystemType = Literal["auto", "standard", "256", "truecolor", "windows"] | None

class RichConsole(Console):
    """Rich console implementation"""
    
    def __init__(self, config: RichConfig | None = None):
        super().__init__(config or RichConfig())
        self._setup_console()
        
    def _setup_console(self) -> None:
        """Setup rich console with config"""
        config = self.config
        if not isinstance(config, RichConfig):
            config = RichConfig()
            
        color_system: ColorSystemType = "auto"  # valor padrão
        
        # Converte o valor da config para um tipo válido se possível
        if config.color_system in ("auto", "standard", "256", "truecolor", "windows"):
            color_system = config.color_system  # type: ignore
            
        self._console = RichConsoleBase(
            style=config.style,
            highlight=config.highlight,
            markup=config.markup,
            emoji=config.emoji,
            color_system=color_system,
            width=config.width,
            height=config.height,
            tab_size=config.tab_size,
            soft_wrap=config.soft_wrap,
        )
        
    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print with rich formatting"""
        self._console.print(*args, **kwargs)
        
    def clear(self) -> None:
        """Clear console"""
        self._console.clear()
        
    def rule(self, title: str = "", **kwargs: Any) -> None:
        """Print horizontal rule"""
        self._console.rule(title, **kwargs)
        
    def print_json(self, data: Any, **kwargs: Any) -> None:
        """Print JSON data"""
        self._console.print_json(data, **kwargs)
