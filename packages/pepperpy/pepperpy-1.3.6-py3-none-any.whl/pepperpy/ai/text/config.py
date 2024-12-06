"""Text processing configuration"""

from dataclasses import asdict, dataclass
from typing import Any

from pepperpy.core.config import ModuleConfig


@dataclass
class TextConfig(ModuleConfig):
    """Configuration for text processing"""

    use_tokenizer: bool = False
    tokenizer_model: str = "gpt2"
    max_chunk_size: int = 1000
    min_chunk_size: int = 100
    overlap: int = 100
    respect_sentences: bool = True

    def dict(self) -> dict[str, Any]:
        """Convert config to dictionary"""
        return asdict(self)
