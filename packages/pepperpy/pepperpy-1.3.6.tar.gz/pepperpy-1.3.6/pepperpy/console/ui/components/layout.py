"""Layout component for UI organization"""

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal, Union

from rich.layout import Layout as RichLayout

from .base import Component


@dataclass
class LayoutConfig:
    """Layout configuration"""

    direction: Literal["horizontal", "vertical"] = "vertical"
    ratios: list[Union[int, float]] | None = None
    minimum_size: int = 1


class Layout(Component):
    """Layout component for organizing UI elements"""

    def __init__(self, config: LayoutConfig | None = None):
        super().__init__()
        self.config = config or LayoutConfig()
        self._layout = RichLayout()
        self._components: list[Component] = []

    async def initialize(self) -> None:
        """Initialize layout"""
        await super().initialize()
        for component in self._components:
            await component.initialize()

    async def split(
        self,
        *components: Component,
        direction: str | None = None,
        ratios: list[Union[int, float]] | None = None,
    ) -> None:
        """Split layout into components"""
        self._components.extend(components)

        # Renderizar os componentes de forma assíncrona
        rendered_components = []
        for comp in components:
            rendered = await comp.render()
            if rendered is not None:
                rendered_components.append(rendered)

        # Criar sublayouts para cada componente
        sublayouts = []
        for i, rendered in enumerate(rendered_components):
            sublayout = RichLayout(name=f"sublayout_{i}")
            sublayout.update(rendered)
            sublayouts.append(sublayout)

        # Configurar o layout principal
        self._layout.split_column(*sublayouts) if (
            direction or self.config.direction
        ) == "vertical" else self._layout.split_row(*sublayouts)

        # Ajustar proporções se fornecidas
        if ratios or self.config.ratios:
            sizes = ratios or self.config.ratios
            if sizes and len(sizes) == len(sublayouts):
                total = sum(sizes)
                for layout, size in zip(sublayouts, sizes):
                    # Converter para inteiros antes de criar o Fraction
                    numerator = int(size * 1000)  # Multiplicar por 1000 para preservar precisão
                    denominator = int(total * 1000)
                    layout.ratio = Fraction(numerator, denominator)

    async def render(self) -> Any:
        """Render layout"""
        await super().render()
        return self._layout

    async def cleanup(self) -> None:
        """Cleanup layout resources"""
        for component in self._components:
            await component.cleanup()
        await super().cleanup()
