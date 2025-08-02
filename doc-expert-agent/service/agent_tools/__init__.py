"""
Tools Agent module - Implementação de conexão com ferramentas externas.
"""

from .connection import ConnectionWithToolsToOpenAI
from .prompt import Prompt

__all__ = ["ConnectionWithToolsToOpenAI", "Prompt"] 