"""Vector cache implementation"""

from typing import Any

import numpy as np
from sklearn.neighbors import NearestNeighbors

from .config import CacheConfig
from .exceptions import CacheError
from .types import VectorEntry


class VectorCache:
    """Cache for vector embeddings"""

    def __init__(self, config: CacheConfig):
        self.config = config
        self._vectors: list[np.ndarray] = []
        self._metadata: list[VectorEntry] = []
        self._index: NearestNeighbors | None = None

    async def initialize(self) -> None:
        """Initialize vector cache"""
        try:
            self._index = NearestNeighbors(
                n_neighbors=min(10, self.config.max_size), metric="cosine",
            )
        except Exception as e:
            raise CacheError(f"Failed to initialize vector cache: {e!s}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup vector cache"""
        self._vectors = []
        self._metadata = []
        self._index = None

    async def add(self, key: str, vector: Any, metadata: dict | None = None) -> None:
        """Add vector to cache"""
        try:
            if self._index is None:
                raise CacheError("Vector cache not initialized")

            vector = np.array(vector).reshape(1, -1)
            self._vectors.append(vector)
            self._metadata.append(VectorEntry(key=key, vector=vector, metadata=metadata or {}))

            if len(self._vectors) > 1:
                self._index.fit(np.vstack(self._vectors))
        except Exception as e:
            raise CacheError(f"Failed to add vector: {e!s}", cause=e)

    async def search(
        self, vector: Any, limit: int = 1, threshold: float = 0.8,
    ) -> list[VectorEntry]:
        """Search for similar vectors"""
        try:
            if not self._vectors or self._index is None:
                return []

            vector = np.array(vector).reshape(1, -1)
            distances, indices = self._index.kneighbors(
                vector, n_neighbors=min(limit, len(self._vectors)),
            )

            results = []
            for dist, idx in zip(distances[0], indices[0], strict=False):
                similarity = 1 - dist
                if similarity >= threshold:
                    results.append(self._metadata[idx])

            return results
        except Exception as e:
            raise CacheError(f"Vector search failed: {e!s}", cause=e)
