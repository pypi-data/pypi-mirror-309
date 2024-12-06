"""Console module for terminal UI"""

from typing import Any

from rich.console import Console as RichConsole
from rich.markup import escape
from rich.panel import Panel
from rich.text import Text


class Console:
    """Console wrapper for Rich console"""

    def __init__(self):
        self._console = RichConsole()

    def clear(self) -> None:
        """Clear console screen"""
        self._console.clear()

    async def print(self, content: Any) -> None:
        """Print content to console"""
        if hasattr(content, "render"):
            rendered_content = await content.render()
            self._console.print(rendered_content)
        else:
            self._console.print(content)

    def success(self, message: str, *, title: str | None = None, content: str | None = None) -> None:
        """Print success message with optional title and content"""
        if title or content:
            text = Text()
            if title:
                text.append(f"{title}\n", style="bold green")
            if content:
                text.append(escape(str(content)))
            self._console.print(Panel(text, style="green"))
        else:
            self._console.print(f"✅ {escape(message)}", style="green bold")

    def error(self, *messages: str) -> None:
        """Print error message"""
        message = " ".join(str(m) for m in messages)
        self._console.print(f"❌ {escape(message)}", style="red bold")

    def warning(self, message: str) -> None:
        """Print warning message"""
        self._console.print(f"⚠️ {escape(message)}", style="yellow bold")

    def info(self, message: str, *, title: str | None = None, subtitle: str | None = None) -> None:
        """Print info message with optional title and subtitle"""
        if title or subtitle:
            text = Text()
            if title:
                text.append(f"{title}\n", style="bold blue")
            if subtitle:
                text.append(f"{subtitle}\n", style="blue")
            text.append(escape(message))
            self._console.print(Panel(text, style="blue"))
        else:
            self._console.print(f"ℹ️ {escape(message)}", style="blue bold")
