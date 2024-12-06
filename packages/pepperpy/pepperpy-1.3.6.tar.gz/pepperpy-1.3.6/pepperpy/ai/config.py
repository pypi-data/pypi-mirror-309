from dataclasses import dataclass


@dataclass
class AIConfig:
    """AI module configuration"""

    provider: str = "mock"
    api_key: str | None = None
    model: str = "default"
