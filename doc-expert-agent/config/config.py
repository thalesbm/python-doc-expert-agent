"""
Configuração centralizada para o Doc Expert Agent.
Configurações otimizadas para desenvolvimento.
"""

from config.database_config import DatabaseConfig
from config.path_config import PathConfig
from config.logging_config import LoggingConfig
from config.openai_config import OpenAIConfig
from config.rag_config import RagConfig
from config.streamlit_config import StreamlitConfig

class Config:
    """Classe principal de configuração para desenvolvimento."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.path = PathConfig()
        self.openai = OpenAIConfig()
        self.rag = RagConfig()
        self.logging = LoggingConfig()
        self.streamlit = StreamlitConfig()

# Instância global de configuração
config = Config()

def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config 