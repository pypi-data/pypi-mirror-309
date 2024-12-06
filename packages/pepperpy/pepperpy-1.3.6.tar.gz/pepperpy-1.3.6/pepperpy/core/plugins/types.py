"""Plugin type definitions"""

from dataclasses import dataclass


@dataclass
class PluginMetadata:
    """Plugin metadata"""

    name: str
    version: str
    description: str
    dependencies: list[str]


@dataclass
class Plugin:
    """Plugin information"""

    metadata: PluginMetadata
    class_: type
