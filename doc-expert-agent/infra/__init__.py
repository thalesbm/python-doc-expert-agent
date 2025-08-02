"""
Infrastructure module - Responsável por configurações de infraestrutura e clientes externos.
"""

from .openai_client import OpenAIClientFactory
from .logger import setup_logging, get_logger, set_log_level, add_file_handler

__all__ = [
    "OpenAIClientFactory",
    "setup_logging",
    "get_logger", 
    "set_log_level",
    "add_file_handler",
] 