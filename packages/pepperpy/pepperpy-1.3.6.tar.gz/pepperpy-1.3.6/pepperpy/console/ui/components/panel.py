"""Panel component for content framing"""

from dataclasses import dataclass
from typing import Any, Literal

from rich.box import ASCII, DOUBLE, HEAVY, ROUNDED, SQUARE  # Importar os estilos de borda do Rich
from rich.panel import Panel as RichPanel

from .base import Component

# Definir tipos literais para estilos de borda válidos
BorderStyle = Literal[
    "none",
    "hidden",
    "ascii",
    "square",
    "heavy",
    "double",
    "rounded",  # Mantemos "rounded" na nossa API
]


@dataclass
class PanelConfig:
    """Panel configuration"""

    title: str = ""
    subtitle: str = ""
    style: str = "none"
    border_style: BorderStyle = "square"
    padding: tuple[int, int] = (1, 1)


class Panel(Component):
    """Panel component for framing content"""

    def __init__(self, content: Any, config: PanelConfig | None = None):
        super().__init__()
        self.content = content
        self.config = config or PanelConfig()

    async def initialize(self) -> None:
        """Initialize panel"""
        await super().initialize()
        if isinstance(self.content, Component):
            await self.content.initialize()

    async def render(self) -> Any:
        """Render panel"""
        await super().render()
        content = (
            await self.content.render() if isinstance(self.content, Component) else self.content
        )

        # Mapear nossos estilos de borda para os estilos do Rich
        box_style = {
            "none": None,
            "hidden": None,
            "ascii": ASCII,
            "square": SQUARE,
            "heavy": HEAVY,
            "double": DOUBLE,
            "rounded": ROUNDED,
        }[self.config.border_style]

        return RichPanel(
            content,
            title=self.config.title,
            subtitle=self.config.subtitle,
            style=self.config.style,
            box=box_style,  # Usar box ao invés de border_style
            padding=self.config.padding,
        )

    async def cleanup(self) -> None:
        """Cleanup panel resources"""
        if isinstance(self.content, Component):
            await self.content.cleanup()
        await super().cleanup()
