"""Network type definitions"""

import json
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientWebSocketResponse


@dataclass
class Request:
    """HTTP request information"""

    method: str
    url: str
    headers: dict[str, str]
    params: dict[str, str]
    data: Any
    timeout: float


@dataclass
class Response:
    """HTTP response information"""

    status: int
    headers: dict[str, str]
    content: bytes
    text: str
    json: dict[str, Any] | None
    elapsed: float


@dataclass
class WebSocket:
    """WebSocket connection"""

    url: str
    connection: ClientWebSocketResponse
    protocols: list[str]

    async def send(self, data: Any) -> None:
        """Send data through WebSocket"""
        await self.connection.send_str(json.dumps(data))

    async def receive(self) -> Any:
        """Receive data from WebSocket"""
        msg = await self.connection.receive_str()
        return json.loads(msg)

    async def close(self) -> None:
        """Close WebSocket connection"""
        await self.connection.close()
