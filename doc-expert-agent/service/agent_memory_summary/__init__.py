"""
Summary Memory Agent module - Implementação de conexão com memória resumida.
"""

from .connection import ConnectionWithSummaryMemoryToOpenAI
from .prompt import Prompt

__all__ = ["ConnectionWithSummaryMemoryToOpenAI", "Prompt"] 