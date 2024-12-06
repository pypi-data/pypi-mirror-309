"""Core type definitions"""

from typing import Any, Union

# Type alias for JSON-serializable dictionary
JsonDict = dict[str, Any]

# Type alias for primitive JSON values
JsonValue = Union[str, int, float, bool, None, dict[str, Any], list]
