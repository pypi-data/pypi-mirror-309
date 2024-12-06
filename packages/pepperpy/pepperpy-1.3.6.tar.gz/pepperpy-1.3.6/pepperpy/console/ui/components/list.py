"""List view component"""

from dataclasses import dataclass
from typing import Generic, TypeVar

from rich.text import Text

from .base import Component

T = TypeVar("T")


@dataclass
class ListItem(Generic[T]):
    """List item configuration"""

    value: T
    label: str
    enabled: bool = True
    style: str = "default"


class ListView(Component, Generic[T]):
    """List view component"""

    def __init__(self):
        super().__init__()
        self._items: list[ListItem[T]] = []

    async def initialize(self) -> None:
        """Initialize list view"""
        await super().initialize()

    async def cleanup(self) -> None:
        """Cleanup list view resources"""
        await super().cleanup()

    def add_item(self, value: T, label: str, enabled: bool = True, style: str = "default") -> None:
        """Add item to list"""
        self._items.append(ListItem(value, label, enabled, style))

    async def render(self) -> Text:
        """Render list view"""
        await super().render()
        text = Text()
        for item in self._items:
            style = item.style if item.enabled else "dim"
            text.append(f"{item.label}\n", style=style)
        return text
