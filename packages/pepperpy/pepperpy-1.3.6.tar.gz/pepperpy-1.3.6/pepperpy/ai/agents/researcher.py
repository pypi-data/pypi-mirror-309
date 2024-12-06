"""Research agent implementation"""

from typing import Any

from ..client import AIClient
from ..templates import PromptTemplate
from ..types import AIResponse
from .base import BaseAgent


class ResearchAgent(BaseAgent):
    """Agent specialized in research and analysis"""

    DEFAULT_TEMPLATES = {
        "research": PromptTemplate(
            "Research Topic: {topic}\n\n"
            "Please conduct a thorough analysis considering:\n"
            "1. Key concepts and definitions\n"
            "2. Main arguments and perspectives\n"
            "3. Supporting evidence\n"
            "4. Potential counterarguments\n"
            "5. Practical implications\n\n"
            "Additional Context: {context}",
        ),
        "summarize": PromptTemplate(
            "Please provide a comprehensive summary of the following content:\n\n{content}\n\n"
            "Focus on:\n"
            "- Main ideas\n"
            "- Key findings\n"
            "- Important conclusions",
        ),
        "evaluate": PromptTemplate(
            "Please evaluate the following content:\n\n{content}\n\n"
            "Consider:\n"
            "- Reliability of sources\n"
            "- Quality of evidence\n"
            "- Potential biases\n"
            "- Logical consistency\n"
            "- Areas for improvement",
        ),
    }

    def __init__(
        self,
        client: AIClient,
        name: str = "Research Assistant",
        description: str = "Specialized in research and analysis",
        system_prompt: str | None = None,
        templates: dict[str, PromptTemplate] | None = None,
    ):
        super().__init__(
            client=client,
            name=name,
            description=description,
            system_prompt=system_prompt
            or (
                "You are a research assistant specialized in conducting thorough "
                "analysis and evaluation of information. Your responses should be "
                "well-structured, evidence-based, and consider multiple perspectives."
            ),
            templates=templates or self.DEFAULT_TEMPLATES,
        )

    async def execute(self, task: str, **kwargs: Any) -> AIResponse:
        """
        Execute research task

        Args:
            task: Research task/topic
            **kwargs: Additional parameters

        Returns:
            AIResponse: Research results

        """
        template = self.get_template("research")
        if not template:
            raise ValueError("Research template not found")

        prompt = template.format(topic=task, **kwargs)
        return await self.client.ask(prompt)

    async def summarize(self, content: str) -> AIResponse:
        """
        Generate summary of content

        Args:
            content: Content to summarize

        Returns:
            AIResponse: Generated summary

        """
        template = self.get_template("summarize")
        if not template:
            raise ValueError("Summarize template not found")

        prompt = template.format(content=content)
        return await self.client.ask(prompt)

    async def evaluate(self, content: str, criteria: str | None = None) -> AIResponse:
        """
        Evaluate quality and reliability of content

        Args:
            content: Content to evaluate
            criteria: Optional additional evaluation criteria

        Returns:
            AIResponse: Evaluation results

        """
        template = self.get_template("evaluate")
        if not template:
            raise ValueError("Evaluate template not found")

        prompt = template.format(content=content, criteria=criteria if criteria else "")
        return await self.client.ask(prompt)
