"""Base agent implementation"""

from abc import ABC, abstractmethod
from typing import Any

from ..client import AIClient
from ..templates import PromptTemplate
from ..types import AIResponse, Message, UsageInfo


class BaseAgent(ABC):
    """Base class for AI agents"""

    def __init__(
        self,
        client: AIClient,
        name: str,
        description: str,
        system_prompt: str | None = None,
        templates: dict[str, PromptTemplate] | None = None,
    ):
        self.client = client
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.templates = templates or {}
        self.conversation: list[Message] = []

        if system_prompt:
            tokens = len(system_prompt.split())
            usage = UsageInfo(prompt_tokens=tokens, completion_tokens=0, total_tokens=tokens)

            self.conversation.append(
                Message(content=system_prompt, sender="system", metadata={"usage": usage}),
            )

    @abstractmethod
    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """Execute agent's primary task"""

    async def think(self, context: str) -> AIResponse:
        """Internal reasoning about a context"""
        template = self.templates.get(
            "think",
            PromptTemplate(
                "Given the context:\n{context}\n\nAnalyze the situation and explain your reasoning.",
            ),
        )
        prompt = template.format(context=context)
        return await self.client.ask(prompt)

    async def plan(self, task: str) -> list[str]:
        """Plan steps to accomplish a task"""
        template = self.templates.get(
            "plan",
            PromptTemplate("Task: {task}\n\nBreak this task into smaller, actionable steps."),
        )
        prompt = template.format(task=task)
        response = await self.client.ask(prompt)
        return [step.strip() for step in response.content.split("\n") if step.strip()]

    def add_template(self, name: str, template: PromptTemplate) -> None:
        """Add new prompt template"""
        self.templates[name] = template

    def get_template(self, name: str) -> PromptTemplate | None:
        """Get prompt template by name"""
        return self.templates.get(name)
