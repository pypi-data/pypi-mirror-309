"""Sentence Transformers embedding provider"""

from typing import List

import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from ..config import EmbeddingConfig
from ..exceptions import EmbeddingError
from ..types import EmbeddingResult
from .base import BaseEmbeddingProvider


class SentenceTransformersProvider(BaseEmbeddingProvider):
    """Sentence Transformers embedding provider implementation"""

    def __init__(self, config: EmbeddingConfig) -> None:
        super().__init__(config)
        self._model: SentenceTransformer | None = None

    async def initialize(self) -> None:
        """Initialize provider"""
        try:
            self._model = SentenceTransformer(self.config.model_name)
        except Exception as e:
            raise EmbeddingError(f"Failed to initialize model: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup provider resources"""
        self._model = None

    async def embed(self, text: str) -> EmbeddingResult:
        """Generate embeddings for text"""
        if not self._model:
            raise EmbeddingError("Model not initialized")

        try:
            # Gerar embeddings
            embeddings = self._model.encode(
                text,
                convert_to_tensor=True,
                normalize_embeddings=True,
            )

            # Converter para numpy e depois para lista
            if isinstance(embeddings, torch.Tensor):
                embeddings_np = embeddings.detach().cpu().numpy()
            else:
                embeddings_np = np.array(embeddings)

            # Converter para float32 e depois para lista
            embeddings_list = embeddings_np.astype(np.float32).tolist()

            return EmbeddingResult(
                embeddings=embeddings_list,
                model=self.config.model_name,
                dimensions=len(embeddings_list),
            )

        except Exception as e:
            raise EmbeddingError(f"Failed to generate embeddings: {e!s}", cause=e)

    async def embed_batch(self, texts: List[str]) -> List[EmbeddingResult]:
        """Generate embeddings for multiple texts"""
        return [await self.embed(text) for text in texts]
