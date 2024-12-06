"""Dialog component"""

from dataclasses import dataclass
from typing import Any, Callable

from rich.box import ROUNDED
from rich.console import Console as RichConsole
from rich.panel import Panel as RichPanel
from rich.text import Text

from .base import Component


@dataclass
class DialogButton:
    """Dialog button configuration"""

    label: str
    callback: Callable[[], None]
    style: str = "default"


class Dialog(Component):
    """Dialog component"""

    def __init__(self):
        super().__init__()
        self.title = ""
        self._content: Any = None
        self._buttons: list[DialogButton] = []
        self._console = RichConsole()

    async def initialize(self) -> None:
        """Initialize dialog"""
        await super().initialize()

    async def cleanup(self) -> None:
        """Cleanup dialog resources"""
        await super().cleanup()

    def add_button(self, label: str, callback: Callable[[], None], style: str = "default") -> None:
        """Add button to dialog"""
        self._buttons.append(DialogButton(label, callback, style))

    @property
    def content(self) -> Any:
        """Get dialog content"""
        return self._content

    @content.setter
    def content(self, value: Any) -> None:
        """Set dialog content"""
        self._content = value

    async def render(self) -> RichPanel:
        """Render dialog"""
        await super().render()
        text = Text()

        # Renderizar o conteúdo
        if isinstance(self._content, Component):
            rendered_content = await self._content.render()
            # Se o conteúdo for um objeto Rich, usar str() para renderizar
            if hasattr(rendered_content, "__rich__"):
                with self._console.capture() as capture:
                    self._console.print(rendered_content)
                text.append(capture.get())
            else:
                text.append(str(rendered_content))
        elif hasattr(self._content, "__rich__"):
            # Se o conteúdo for um objeto Rich (como Text), renderizar diretamente
            with self._console.capture() as capture:
                self._console.print(self._content)
            text.append(capture.get())
        else:
            text.append(str(self._content))

        # Adicionar botões
        if self._buttons:
            text.append("\n\n")
            for btn in self._buttons:
                text.append(f"[{btn.style}]{btn.label}[/] ")

        return RichPanel(text, title=self.title, box=ROUNDED, style="blue")
