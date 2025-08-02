"""
Chunk module - Responsável por diferentes estratégias de chunking de documentos.
"""

from .chunk_fixed import FixedChunker
from .chunk_adaptive import AdaptiveChunker
from .splitter import Splitter
from .chunk_utils import remove_duplicate_chunks

__all__ = [
    "FixedChunker",
    "AdaptiveChunker", 
    "Splitter",
    "remove_duplicate_chunks"
] 