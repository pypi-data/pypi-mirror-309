"""Embedding types and models"""

from dataclasses import dataclass
from typing import List, NewType

# Tipos básicos
EmbeddingVector = NewType("EmbeddingVector", List[float])
EmbeddingBatch = NewType("EmbeddingBatch", List[EmbeddingVector])


@dataclass
class EmbeddingResult:
    """Result from embedding generation"""
    embeddings: EmbeddingVector
    model: str
    dimensions: int


@dataclass
class EmbeddingBatchResult:
    """Result from batch embedding generation"""
    embeddings: EmbeddingBatch
    model: str
    dimensions: int
