"""Schema validation utilities"""

from typing import Any

from pydantic import BaseModel, ValidationError

from pepperpy.core.exceptions import PepperPyError


class SchemaError(PepperPyError):
    """Schema validation error"""


class SchemaValidator:
    """Schema validator using Pydantic models"""

    def __init__(self, schema: type[BaseModel]):
        self.schema = schema

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate data against schema

        Args:
            data: Data to validate

        Returns:
            Dict[str, Any]: Validated data

        Raises:
            SchemaError: If validation fails

        """
        try:
            model = self.schema(**data)
            return model.model_dump()
        except ValidationError as e:
            raise SchemaError(f"Schema validation failed: {e!s}")
