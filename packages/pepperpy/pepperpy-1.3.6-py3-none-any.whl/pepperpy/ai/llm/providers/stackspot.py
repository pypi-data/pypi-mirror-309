"""StackSpot AI LLM provider"""

from collections.abc import AsyncIterator

import httpx

from pepperpy.ai.llm.exceptions import ProviderError
from pepperpy.ai.llm.types import LLMConfig, LLMResponse, Message

from .base import BaseLLMProvider


class StackSpotConfig(LLMConfig):
    """StackSpot AI provider configuration"""

    def __init__(
        self,
        account_slug: str,
        client_id: str,
        client_key: str,
        qc_slug: str,
        model: str = "stackspot-ai",
        base_url: str = "https://genai-code-buddy-api.stackspot.com/v1",
        auth_url: str = "https://idm.stackspot.com",
    ) -> None:
        if not all([account_slug, client_id, client_key, qc_slug]):
            raise ValueError("All StackSpot credentials are required")

        super().__init__(
            provider="stackspot",
            api_key=client_key,
            model=model,
        )
        self.account_slug = account_slug
        self.client_id = client_id
        self.client_key = client_key
        self.qc_slug = qc_slug
        self.base_url = base_url
        self.auth_url = auth_url


class StackSpotProvider(BaseLLMProvider):
    """StackSpot AI LLM provider implementation"""

    def __init__(self, config: StackSpotConfig | None = None) -> None:
        if not config:
            raise ValueError("StackSpot configuration is required")

        self.config = config
        self._client: httpx.AsyncClient | None = None
        self._token: str | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        self._client = httpx.AsyncClient(base_url=self.config.base_url)
        await self._get_token()

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        if self._client:
            await self._client.aclose()
            self._client = None
        self._token = None

    async def _get_token(self) -> str:
        """
        Get access token

        Returns:
            str: Access token

        Raises:
            ProviderError: If token cannot be obtained

        """
        try:
            if not self._token:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.config.auth_url}/{self.config.account_slug}/oidc/oauth/token",
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                        data={
                            "client_id": self.config.client_id,
                            "grant_type": "client_credentials",
                            "client_secret": self.config.client_key,
                        },
                    )
                    response.raise_for_status()
                    data = response.json()
                    if not data.get("access_token"):
                        raise ProviderError("Invalid token response")
                    self._token = data["access_token"]

            if not self._token:  # Verificação adicional após tentativa de obtenção
                raise ProviderError("Failed to obtain access token")

            return self._token

        except Exception as e:
            raise ProviderError("Failed to get access token", cause=e)

    async def complete(self, messages: list[Message]) -> LLMResponse:
        """Complete chat messages using Quick Command"""
        if not self._client:
            raise ProviderError("Provider not initialized")

        try:
            token = await self._get_token()

            # Create Quick Command execution
            response = await self._client.post(
                f"/quick-commands/create-execution/{self.config.qc_slug}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                json={
                    "input_data": "\n".join(
                        msg["content"] for msg in messages if msg["role"] == "user"
                    ),
                },
            )
            response.raise_for_status()
            execution_id = response.json()

            # Get execution result
            response = await self._client.get(
                f"/quick-commands/execution/{execution_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            response.raise_for_status()
            data = response.json()

            return LLMResponse(
                content=data["answer"],
                model=self.config.model,
                usage={},
                metadata=data,
            )
        except Exception as e:
            raise ProviderError("Failed to execute Quick Command", cause=e)

    async def stream(self, messages: list[Message]) -> AsyncIterator[LLMResponse]:
        """Stream is not supported by StackSpot AI"""
        raise ProviderError("Streaming not supported by StackSpot AI")
