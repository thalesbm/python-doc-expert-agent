"""
Configuração centralizada para o Doc Expert Agent.
Configurações otimizadas para desenvolvimento.
"""

from dataclasses import dataclass
import os

@dataclass
class DatabaseConfig:
    """Configurações de banco de dados e RAG."""
    tcc_path: str = "files/tcc/chroma_db/"
    hp_path: str = "files/hp/chroma_db/"
    chunk_size: int = 1024
    chunk_overlap: int = 150
    top_k: int = 5 
    fetch_k: int = 20
    score_threshold: float = 0.85

@dataclass
class PathConfig:
    """Configurações de caminhos."""
    tcc_path: str = "files/tcc.pdf"
    hp_path: str = "files/harry-potter-1-cap-1.pdf"

@dataclass
class OpenAIConfig:
    """Configurações da OpenAI."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: int = 1000

@dataclass
class RagConfig:
    """Configurações do sistema RAG."""
    retrieval_strategy: int = 10
    max_context_length: int = 2000
    enable_evaluation: bool = True
    evaluation_metrics: list = None

    def __post_init__(self):
        if self.evaluation_metrics is None:
            self.evaluation_metrics = ["answer_relevancy", "faithfulness"]

@dataclass
class LoggingConfig:
    """Configurações de logging."""
    level: str = "DEBUG"
    format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    file_path: str = os.getenv("LOG_FILE", "app.log")

@dataclass
class StreamlitConfig:
    """Configurações do Streamlit."""
    page_title: str = "Doc Expert Agent"
    page_icon: str = ""
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"

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