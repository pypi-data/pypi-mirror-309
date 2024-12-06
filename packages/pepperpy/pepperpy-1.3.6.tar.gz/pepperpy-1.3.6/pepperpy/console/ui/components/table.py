"""Table component"""

from dataclasses import dataclass
from typing import Literal

from rich.box import SIMPLE
from rich.table import Table as RichTable

from .base import Component

# Definir tipos literais para alinhamento
AlignMethod = Literal["left", "center", "right"]
JustifyMethod = Literal["left", "center", "right", "full", "default"]


@dataclass
class Column:
    """Table column configuration"""

    header: str
    style: str | None = None
    align: AlignMethod = "left"
    show_header: bool = True


@dataclass
class TableConfig:
    """Table configuration"""

    title: str = ""
    style: str = "default"
    show_header: bool = True
    box = SIMPLE
    padding: tuple[int, int] = (0, 1)


class Table(Component):
    """Table component"""

    def __init__(self, config: TableConfig | None = None):
        super().__init__()
        self.config = config or TableConfig()
        self._table = RichTable(
            title=self.config.title,
            style=self.config.style,
            show_header=self.config.show_header,
            box=self.config.box,
            padding=self.config.padding,
        )
        self._columns: list[Column] = []
        self._rows: list[tuple[str, ...]] = []

    async def initialize(self) -> None:
        """Initialize table"""
        await super().initialize()

    async def cleanup(self) -> None:
        """Cleanup table resources"""
        await super().cleanup()

    def add_column(
        self,
        header: str,
        *,
        style: str | None = None,
        align: AlignMethod = "left",
        show_header: bool = True,
    ) -> None:
        """Add column to table"""
        self._columns.append(Column(header, style, align, show_header))
        # Converter AlignMethod para JustifyMethod (são compatíveis neste caso)
        justify: JustifyMethod = align
        self._table.add_column(
            header if show_header else "",
            style=style,
            justify=justify,
            header_style=style,  # Adicionar estilo ao cabeçalho também
        )

    def add_row(self, *values: str) -> None:
        """Add row to table"""
        self._rows.append(values)
        self._table.add_row(*values)

    async def render(self) -> RichTable:
        """Render table"""
        await super().render()
        # Recria a tabela para garantir estado limpo
        table = RichTable(
            title=self.config.title,
            style=self.config.style,
            show_header=self.config.show_header,
            box=self.config.box,
            padding=self.config.padding,
        )

        # Adiciona as colunas
        for col in self._columns:
            justify: JustifyMethod = col.align
            table.add_column(
                col.header if col.show_header else "",
                style=col.style,
                justify=justify,
                header_style=col.style,
            )

        # Adiciona as linhas
        for row in self._rows:
            table.add_row(*row)

        return table
