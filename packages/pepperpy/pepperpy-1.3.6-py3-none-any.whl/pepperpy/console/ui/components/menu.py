"""Menu component for navigation"""

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from rich.text import Text

from .base import Component

T = TypeVar("T")


@dataclass
class MenuItem(Generic[T]):
    """Menu item configuration"""

    label: str
    value: T
    callback: Callable[[], None]
    enabled: bool = True
    style: str = "default"
    shortcut: str | None = None


class Menu(Component, Generic[T]):
    """Menu component"""

    def __init__(self):
        super().__init__()
        self._items: list[MenuItem[T]] = []
        self._selected_index: int = 0
        self._active: bool = False

    def add_item(
        self,
        label: str,
        value: T,
        callback: Callable[[], None],
        enabled: bool = True,
        style: str = "default",
        shortcut: str | None = None,
    ) -> None:
        """Add menu item"""
        self._items.append(MenuItem(label, value, callback, enabled, style, shortcut))

    def select_next(self) -> None:
        """Select next menu item"""
        if not self._items:
            return
        self._selected_index = (self._selected_index + 1) % len(self._items)

    def select_previous(self) -> None:
        """Select previous menu item"""
        if not self._items:
            return
        self._selected_index = (self._selected_index - 1) % len(self._items)

    def activate(self) -> None:
        """Activate menu"""
        self._active = True

    def deactivate(self) -> None:
        """Deactivate menu"""
        self._active = False

    def activate_selected(self) -> None:
        """Activate selected menu item"""
        if not self._items:
            return

        if 0 <= self._selected_index < len(self._items):
            item = self._items[self._selected_index]
            if item.enabled:
                item.callback()

    async def render(self) -> Any:
        """Render menu"""
        await super().render()

        text = Text()
        for i, item in enumerate(self._items):
            # Add selection indicator
            prefix = ">" if i == self._selected_index and self._active else " "
            text.append(f"{prefix} ", style="bold")

            # Add shortcut if available
            if item.shortcut:
                text.append(f"[{item.shortcut}] ", style="dim")

            # Add item label with style
            style = item.style
            if not item.enabled:
                style = "dim " + style
            if i == self._selected_index and self._active:
                style = "bold " + style

            text.append(f"{item.label}\n", style=style)

        return text
