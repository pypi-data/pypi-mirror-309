"""Data transformation utilities"""

from collections.abc import Callable
from typing import Any, TypeVar, Union

from pepperpy.core.exceptions import PepperPyError


class TransformError(PepperPyError):
    """Transform error"""


T = TypeVar("T")
TransformValue = Union[str, list[Any], Any]
TransformOptions = dict[str, Any]
TransformFunc = Callable[[TransformValue, TransformOptions], TransformValue]


class Transformer:
    """Data transformer"""

    def __init__(self) -> None:
        self._transforms: dict[str, TransformFunc] = {}
        self._register_default_transforms()

    def _register_default_transforms(self) -> None:
        """Register default transforms"""
        self._transforms.update(
            {
                "format": self._format_transform,
                "replace": self._replace_transform,
                "filter": self._filter_transform,
                "map": self._map_transform,
            },
        )

    def transform(
        self, value: TransformValue, transform: str, options: dict[str, Any] | None = None,
    ) -> TransformValue:
        """
        Transform value using specified transform

        Args:
            value: Value to transform
            transform: Transform to apply
            options: Transform options

        Returns:
            Any: Transformed value

        Raises:
            TransformError: If transform fails

        """
        try:
            if transform not in self._transforms:
                raise TransformError(f"Unknown transform: {transform}")

            transform_func = self._transforms[transform]
            return transform_func(value, options or {})
        except Exception as e:
            raise TransformError(f"Transform failed: {e!s}", cause=e)

    def _format_transform(self, value: TransformValue, options: TransformOptions) -> str:
        """Format value using template"""
        template = options.get("template", "{}")
        if isinstance(value, (str, int, float)):
            return template.format(value)
        return template.format(str(value))

    def _replace_transform(self, value: TransformValue, options: TransformOptions) -> str:
        """Replace substring in value"""
        if not isinstance(value, str):
            value = str(value)
        old = options.get("old", "")
        new = options.get("new", "")
        return value.replace(old, new)

    def _filter_transform(self, value: TransformValue, options: TransformOptions) -> list[Any]:
        """Filter list using predicate"""
        if not isinstance(value, list):
            raise TransformError("Value must be a list")
        predicate = options.get("predicate", lambda x: bool(x))
        return list(filter(predicate, value))

    def _map_transform(self, value: TransformValue, options: TransformOptions) -> list[Any]:
        """Map function over list"""
        if not isinstance(value, list):
            raise TransformError("Value must be a list")
        func = options.get("func", lambda x: x)
        return list(map(func, value))


# Global transformer instance
transformer = Transformer()
