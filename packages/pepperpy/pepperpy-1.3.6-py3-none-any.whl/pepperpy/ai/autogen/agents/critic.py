from typing import Any

from ...client import AIClient
from ...types import AIResponse, UsageInfo
from ..types import Message
from .base import AutoGenAgent


class CriticAgent(AutoGenAgent):
    """Agent specialized in code review and quality assessment"""

    def __init__(
        self,
        name: str = "Code Reviewer",
        client: AIClient | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            role="critic",
            instructions=kwargs.pop("instructions", ""),
            client=client,
            **kwargs,
        )

    async def _generate_response(self, message: Message) -> AIResponse:
        """Generate review response"""
        if not self.client:
            raise ValueError("Client is required for generating responses")

        prompt = f"""As a code reviewer, analyze this implementation:

{message.content}

Evaluate:
1. Code quality
2. Best practices
3. Performance
4. Security
5. Documentation

Provide specific feedback and suggestions for improvement.
"""
        response = await self.client.ask(prompt)
        return AIResponse(
            content=response.content,
            model=self.client.model,
            usage=UsageInfo(
                prompt_tokens=len(prompt.split()),
                completion_tokens=len(response.content.split()),
                total_tokens=len(prompt.split()) + len(response.content.split()),
            ),
        )
