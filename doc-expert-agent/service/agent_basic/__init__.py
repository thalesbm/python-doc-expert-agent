"""
Basic Agent module - Implementação de conexão básica com LLM.
"""

from .connection import BasicConnectionToOpenAI
from .prompt import Prompt

__all__ = ["BasicConnectionToOpenAI", "Prompt"] 