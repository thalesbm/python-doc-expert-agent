"""
Pipeline module - Contém os componentes do pipeline RAG (Loader, Splitter, Embedding, Retrieval, OpenAI, Evaluate).
"""

from .loader import Loader
from .splitter import Splitter
from .embedding.embedding import Embedding
from .retrieval import Retrieval
from .openai import Key
from .evaluate import Evaluate
from .adaptive_chunker import AdaptiveChunker
from .relevance_filter import RelevanceFilter
from .embedding.embedding_cache import EmbeddingCache

__all__ = [
    "Loader", 
    "Splitter", 
    "Embedding",
    "Retrieval", 
    "Key", 
    "Evaluate",
    "AdaptiveChunker",
    "RelevanceFilter", 
    "EmbeddingCache"
] 