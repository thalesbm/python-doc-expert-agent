"""
Complete Memory Agent module - Implementação de conexão com memória completa.
"""

from .connection import ConnectionWithCompleteMemoryToOpenAI
from .prompt import Prompt

__all__ = ["ConnectionWithCompleteMemoryToOpenAI", "Prompt"] 