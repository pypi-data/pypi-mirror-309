"""Form component for data input"""

from dataclasses import dataclass, field
from typing import Any, Callable

from rich.text import Text

from .base import Component
from .button import Button, ButtonConfig


@dataclass
class FormField:
    """Form field configuration"""

    name: str
    label: str
    required: bool = True
    validators: list[Callable[[str], bool]] = field(default_factory=list)
    default: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class Form(Component):
    """Form component for data input"""

    def __init__(self):
        super().__init__()
        self._fields: list[FormField] = []
        self._values: dict[str, str] = {}
        self._buttons: list[Button] = []
        self._errors: dict[str, list[str]] = {}

    async def initialize(self) -> None:
        """Initialize form"""
        await super().initialize()
        for button in self._buttons:
            await button.initialize()

    def add_field(self, field: FormField) -> None:
        """Add field to form"""
        self._fields.append(field)
        if field.default:
            self._values[field.name] = field.default

    def add_button(self, label: str, callback: Callable[[], None], style: str = "default") -> None:
        """Add button to form"""
        config = ButtonConfig(
            label=label,
            callback=callback,
            style=style
        )
        button = Button(config)
        self._buttons.append(button)

    def get_value(self, field_name: str) -> str:
        """Get field value"""
        return self._values.get(field_name, "")

    def set_value(self, field_name: str, value: str) -> None:
        """Set field value"""
        if any(form_field.name == field_name for form_field in self._fields):
            self._values[field_name] = value
            self._validate_field(field_name)

    def _validate_field(self, field_name: str) -> bool:
        """Validate field value"""
        field = next(form_field for form_field in self._fields if form_field.name == field_name)
        value = self._values.get(field_name, "")

        errors = []
        if field.required and not value:
            errors.append("This field is required")

        for validator in field.validators:
            if not validator(value):
                errors.append("Validation failed")

        self._errors[field_name] = errors
        return not errors

    async def render(self) -> Any:
        """Render form"""
        await super().render()

        text = Text()
        for form_field in self._fields:
            # Add field label
            text.append(f"{form_field.label}: ", style="bold")

            # Add field value or placeholder
            value = self._values.get(form_field.name, "")
            if value:
                text.append(f"{value}\n")
            else:
                text.append("[dim]<empty>[/]\n")

            # Add field errors if any
            if form_field.name in self._errors and self._errors[form_field.name]:
                for error in self._errors[form_field.name]:
                    text.append(f"  [red]• {error}[/]\n")

        # Add buttons
        if self._buttons:
            text.append("\n")
            for button in self._buttons:
                text.append(await button.render())
                text.append(" ")

        return text

    async def cleanup(self) -> None:
        """Cleanup form resources"""
        for button in self._buttons:
            await button.cleanup()
        await super().cleanup()
