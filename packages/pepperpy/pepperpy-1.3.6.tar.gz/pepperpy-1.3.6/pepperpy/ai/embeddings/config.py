"""Embedding configuration"""

from dataclasses import dataclass


@dataclass
class EmbeddingConfig:
    """Configuration for embedding providers"""
    model_name: str
    provider: str = "sentence_transformers"
    normalize: bool = True
    batch_size: int = 32
