"""Configuration management"""

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv


@dataclass
class ConfigField:
    """Configuration field definition"""

    required: bool = False
    default: Any = None
    validator: Callable[[str], bool] | None = None
    error: str | None = None
    description: str | None = None


class Config:
    """Configuration manager"""

    def __init__(self, fields: dict[str, dict[str, Any]]):
        load_dotenv()
        self._fields = {k: ConfigField(**v) for k, v in fields.items()}
        self._values: dict[str, Any] = {}
        self._errors: dict[str, str] = {}
        self._load_values()

    def _load_values(self) -> None:
        for key, field in self._fields.items():
            value = os.getenv(key, field.default)

            if value is None and field.required:
                self._errors[key] = f"Missing required environment variable: {key}"
                continue

            if value and field.validator and not field.validator(value):
                self._errors[key] = field.error or f"Invalid value for {key}"
                continue

            self._values[key] = value

    def is_valid(self) -> bool:
        return len(self._errors) == 0

    def get_errors(self) -> dict[str, str]:
        return self._errors

    def as_dict(self) -> dict[str, Any]:
        return self._values.copy()


def load_config(fields: dict[str, dict[str, Any]]) -> Config:
    """Load configuration from environment variables"""
    return Config(fields)
