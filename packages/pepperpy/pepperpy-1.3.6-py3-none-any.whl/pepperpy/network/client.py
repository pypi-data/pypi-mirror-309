"""Network client implementation"""

import asyncio
import ssl
from collections.abc import AsyncIterator
from dataclasses import asdict
from pathlib import Path
from typing import Any, Protocol

import aiohttp
from aiohttp import ClientTimeout

from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import NetworkConfig
from .exceptions import NetworkError
from .types import Response, WebSocket


class ProgressCallback(Protocol):
    async def __call__(self, downloaded: int, total: int) -> None: ...


class NetworkClient(BaseModule):
    """Client for network operations"""

    def __init__(self, config: NetworkConfig | None = None) -> None:
        super().__init__()
        self.metadata = ModuleMetadata(
            name="network",
            version="1.0.0",
            description="Network operations",
            dependencies=["aiohttp>=3.9.0"],
            config=asdict(config) if config else {},
        )
        self._session: aiohttp.ClientSession | None = None
        self._ws_connections: dict[str, WebSocket] = {}

    async def _setup(self) -> None:
        """Initialize network client"""
        try:
            # Setup SSL context if needed
            ssl_context = None
            if self.config.get("verify_ssl"):
                ssl_context = ssl.create_default_context()
                if cert_path := self.config.get("cert_path"):
                    ssl_context.load_cert_chain(cert_path)

            # Create session with custom settings
            timeout = aiohttp.ClientTimeout(
                total=self.config.get("timeout", 30),
                connect=self.config.get("connect_timeout", 10),
            )

            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers=self.config.get("default_headers", {}),
                cookies=self.config.get("cookies", {}),
                connector=aiohttp.TCPConnector(
                    ssl=ssl_context,
                    limit=self.config.get("max_connections", 100),
                    ttl_dns_cache=self.config.get("dns_cache_ttl", 10),
                ),
            )

        except Exception as e:
            raise NetworkError("Failed to initialize network client", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup network resources"""
        if self._session:
            await self._session.close()
        for ws in self._ws_connections.values():
            await ws.close()

    async def request(self, method: str, url: str, **kwargs) -> Response:
        """Make HTTP request"""
        if not self._session:
            raise NetworkError("Session not initialized")

        try:
            retries = kwargs.pop("retries", self.config.get("max_retries", 3))
            backoff = kwargs.pop("backoff", self.config.get("retry_backoff", 1.0))

            for attempt in range(retries):
                try:
                    start_time = asyncio.get_event_loop().time()
                    async with self._session.request(method, url, **kwargs) as resp:
                        content = await resp.read()
                        text = await resp.text()
                        json_data = (
                            await resp.json() if "application/json" in resp.content_type else None
                        )
                        elapsed = asyncio.get_event_loop().time() - start_time

                        return Response(
                            status=resp.status,
                            headers=dict(resp.headers),
                            content=content,
                            text=text,
                            json=json_data,
                            elapsed=elapsed,
                        )
                except Exception:
                    if attempt == retries - 1:
                        raise
                    await asyncio.sleep(backoff * (2**attempt))

            raise NetworkError("Max retries exceeded")

        except Exception as e:
            raise NetworkError(f"Request failed: {e!s}", cause=e)

    async def download_file(
        self,
        url: str,
        path: str | Path,
        chunk_size: int = 8192,
        progress_callback: ProgressCallback | None = None,
    ) -> Path:
        """Download file with progress tracking"""
        if not self._session:
            raise NetworkError("Session not initialized")

        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            async with self._session.get(url) as response:
                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                with path.open("wb") as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback:
                            await progress_callback(downloaded, total_size)

            return path

        except Exception as e:
            raise NetworkError(f"Download failed: {e!s}", cause=e)

    async def websocket_connect(
        self,
        url: str,
        protocols: list[str] | None = None,
        **kwargs,
    ) -> WebSocket:
        """Create WebSocket connection"""
        if not self._session:
            raise NetworkError("Session not initialized")

        try:
            ws = await self._session.ws_connect(url, protocols=protocols or [], **kwargs)

            connection = WebSocket(url=url, connection=ws, protocols=protocols or [])

            self._ws_connections[url] = connection
            return connection

        except Exception as e:
            raise NetworkError(f"WebSocket connection failed: {e!s}", cause=e)

    async def stream_request(
        self,
        method: str,
        url: str,
        chunk_size: int = 8192,
        **kwargs,
    ) -> AsyncIterator[bytes]:
        """Stream response data"""
        if not self._session:
            raise NetworkError("Session not initialized")

        try:
            async with self._session.request(method, url, **kwargs) as response:
                async for chunk in response.content.iter_chunked(chunk_size):
                    yield chunk

        except Exception as e:
            raise NetworkError(f"Stream request failed: {e!s}", cause=e)

    async def graphql_query(
        self,
        url: str,
        query: str,
        variables: dict[str, Any] | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        """Execute GraphQL query"""
        try:
            response = await self.request(
                "POST",
                url,
                json={"query": query, "variables": variables},
                **kwargs,
            )

            if response.status != 200:
                raise NetworkError(f"GraphQL query failed: {response.text}")

            if not response.json:
                raise NetworkError("Invalid JSON response")

            result = response.json
            if "errors" in result:
                raise NetworkError(f"GraphQL errors: {result['errors']}")

            if "data" not in result:
                raise NetworkError("Missing data in GraphQL response")

            return result["data"]

        except Exception as e:
            raise NetworkError(f"GraphQL request failed: {e!s}", cause=e)

    async def health_check(self, urls: list[str], timeout: float = 5.0) -> dict[str, bool]:
        """Check health of multiple endpoints"""
        if not self._session:
            raise NetworkError("Session not initialized")

        try:

            async def check_url(url: str) -> tuple[str, bool]:
                try:
                    timeout_obj = ClientTimeout(total=timeout)
                    response = await self.request("GET", url, timeout=timeout_obj)
                    return url, 200 <= response.status < 400
                except Exception:
                    return url, False

            tasks = [check_url(url) for url in urls]
            results = await asyncio.gather(*tasks)
            return dict(results)

        except Exception as e:
            raise NetworkError(f"Health check failed: {e!s}", cause=e)

    async def rate_limit(self, requests_per_second: float) -> None:
        """Apply rate limiting"""
        if not hasattr(self, "_last_request_time"):
            self._last_request_time = 0

        now = asyncio.get_event_loop().time()
        elapsed = now - self._last_request_time
        min_interval = 1.0 / requests_per_second

        if elapsed < min_interval:
            await asyncio.sleep(min_interval - elapsed)

        self._last_request_time = asyncio.get_event_loop().time()
