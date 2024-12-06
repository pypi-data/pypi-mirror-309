"""Serialization utilities"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

import msgpack


class DateTimeHandler:
    """Handler for datetime serialization"""

    @staticmethod
    def serialize(obj: Any) -> str | Any:
        """Serialize datetime objects"""
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        return obj

    @staticmethod
    def deserialize(obj: dict[str, Any]) -> datetime | dict[str, Any]:
        """Deserialize datetime objects"""
        if "__datetime__" in obj:
            return datetime.fromisoformat(obj["__datetime__"])
        return obj


class BaseSerializer(ABC):
    """Base class for serializers"""

    def __init__(self, encoding: str = "utf-8", pretty: bool = False):
        self.encoding = encoding
        self.pretty = pretty

    @abstractmethod
    def serialize(self, data: Any) -> bytes:
        """Serialize data to bytes"""

    @abstractmethod
    def deserialize(self, data: bytes) -> Any:
        """Deserialize data from bytes"""


class JsonSerializer(BaseSerializer):
    """JSON serializer implementation"""

    def serialize(self, data: Any) -> bytes:
        """Serialize to JSON"""
        json_kwargs: dict[str, Any] = {
            "default": DateTimeHandler.serialize,
            "ensure_ascii": False,
            "check_circular": True,
            "allow_nan": True,
            "sort_keys": False,
        }

        if self.pretty:
            json_kwargs["indent"] = 2
            json_kwargs["separators"] = (",", ": ")
        else:
            json_kwargs["separators"] = (",", ":")

        return json.dumps(data, **json_kwargs).encode(self.encoding)

    def deserialize(self, data: bytes) -> Any:
        """Deserialize from JSON"""
        return json.loads(
            data.decode(self.encoding), object_hook=DateTimeHandler.deserialize,
        )


class JsonOnlySerializer(BaseSerializer):
    """Safe JSON-only serializer implementation"""

    def __init__(self, encoding: str = "utf-8", pretty: bool = False):
        super().__init__(encoding, pretty)
        self.json_serializer = JsonSerializer(encoding, pretty)

    def serialize(self, data: Any) -> bytes:
        return self.json_serializer.serialize(data)

    def deserialize(self, data: bytes) -> Any:
        return self.json_serializer.deserialize(data)


class MsgPackSerializer(BaseSerializer):
    """MessagePack serializer implementation"""

    def serialize(self, data: Any) -> bytes:
        """Serialize to MessagePack"""
        packed = msgpack.packb(
            data,
            default=DateTimeHandler.serialize,
            use_bin_type=True,
            strict_types=True,
        )
        if packed is None:
            raise ValueError("MessagePack serialization failed")
        return packed

    def deserialize(self, data: bytes) -> Any:
        """Deserialize from MessagePack"""
        return msgpack.unpackb(data, object_hook=DateTimeHandler.deserialize, raw=False)


def get_serializer(format: str = "json", **kwargs: Any) -> BaseSerializer:
    """Get serializer instance"""
    serializers = {
        "json": JsonSerializer,
        "json-only": JsonOnlySerializer,
        "msgpack": MsgPackSerializer,
    }

    if format not in serializers:
        raise ValueError(f"Unsupported format: {format}")

    return serializers[format](**kwargs)
