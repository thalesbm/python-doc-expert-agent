"""
Embedding module - Responsável por geração e cache de embeddings.
"""

from .embedding import Embedding
from .embedding_cache import EmbeddingCache

__all__ = [
    "Embedding",
    "EmbeddingCache"
] 