"""Mock implementations for external resources"""

import asyncio
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockRequest:
    """Mock HTTP request"""

    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)
    data: Any = None


@dataclass
class MockResponse:
    """Mock HTTP response"""

    status: int
    data: Any
    headers: dict[str, str] = field(default_factory=dict)


class MockHTTPClient:
    """Mock HTTP client"""

    def __init__(self):
        self._responses: dict[str, list[MockResponse]] = {}
        self._requests: list[MockRequest] = []
        self._delay: float | None = None

    def add_response(self, url: str, response: MockResponse, method: str = "GET") -> None:
        """Add mock response"""
        key = f"{method}:{url}"
        if key not in self._responses:
            self._responses[key] = []
        self._responses[key].append(response)

    def set_delay(self, seconds: float) -> None:
        """Set response delay"""
        self._delay = seconds

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        data: Any = None,
    ) -> MockResponse:
        """Make mock request"""
        request = MockRequest(
            method=method, url=url, headers=headers or {}, params=params or {}, data=data,
        )
        self._requests.append(request)

        key = f"{method}:{url}"
        if key not in self._responses:
            raise ValueError(f"No mock response for {key}")

        if self._delay:
            await asyncio.sleep(self._delay)

        responses = self._responses[key]
        return responses.pop(0) if responses else responses[0]

    def get_requests(self) -> list[MockRequest]:
        """Get recorded requests"""
        return self._requests

    def clear(self) -> None:
        """Clear mock data"""
        self._responses.clear()
        self._requests.clear()
        self._delay = None


class MockDatabase:
    """Mock database"""

    def __init__(self):
        self._data: dict[str, dict[str, Any]] = {}
        self._queries: list[str] = []

    async def execute(
        self, query: str, params: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute mock query"""
        self._queries.append(query)
        return []

    async def insert(self, table: str, data: dict[str, Any]) -> None:
        """Insert mock data"""
        if table not in self._data:
            self._data[table] = {}
        self._data[table][str(len(self._data[table]))] = data

    async def select(
        self, table: str, conditions: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Select mock data"""
        if table not in self._data:
            return []

        results = []
        for record in self._data[table].values():
            if not conditions or all(record.get(k) == v for k, v in conditions.items()):
                results.append(record)
        return results

    def get_queries(self) -> list[str]:
        """Get recorded queries"""
        return self._queries

    def clear(self) -> None:
        """Clear mock data"""
        self._data.clear()
        self._queries.clear()
