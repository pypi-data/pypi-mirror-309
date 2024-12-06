"""Configuration validation utilities"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ValidationError


@dataclass
class ValidationRule:
    """Custom validation rule"""

    field: str
    validator: Callable[[Any], bool]
    message: str


class ConfigValidator:
    """Configuration validator"""

    def __init__(self):
        self._rules: list[ValidationRule] = []

    def add_rule(self, field: str, validator: Callable[[Any], bool], message: str) -> None:
        """Add custom validation rule"""
        self._rules.append(ValidationRule(field, validator, message))

    def validate(self, config: dict[str, Any], schema: type[BaseModel]) -> BaseModel:
        """Validate configuration against schema and rules"""
        try:
            # First validate against Pydantic model
            validated = schema(**config)

            # Then check custom rules
            errors = []
            for rule in self._rules:
                value = config.get(rule.field)
                if value is not None and not rule.validator(value):
                    errors.append(f"{rule.field}: {rule.message}")

            if errors:
                raise ValueError("\n".join(errors))

            return validated

        except ValidationError as e:
            raise ValueError(f"Invalid configuration: {e!s}")
        except Exception as e:
            raise ValueError(f"Validation failed: {e!s}")
