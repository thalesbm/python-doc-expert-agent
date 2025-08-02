"""
Configuração centralizada para o Doc Expert Agent.
Configurações otimizadas para desenvolvimento.
"""

import os
from typing import Optional
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Configurações de banco de dados e RAG."""
    tcc_path: str = "files/tcc/chroma_db/"
    hp_path: str = "files/hp/chroma_db/"
    chunk_size: int = 512  # Otimizado para desenvolvimento
    chunk_overlap: int = 100
    top_k: int = 3  # Menos documentos para desenvolvimento
    fetch_k: int = 10
    score_threshold: float = 0.8


@dataclass
class OpenAIConfig:
    """Configurações da OpenAI."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.1  # Pequena variação para desenvolvimento
    max_tokens: int = 1000  # Limite menor para desenvolvimento
    api_key: Optional[str] = None


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
    level: str = "DEBUG"  # DEBUG para desenvolvimento
    format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    file_path: str = "logs/dev.log"

@dataclass
class StreamlitConfig:
    """Configurações do Streamlit."""
    page_title: str = "Doc Expert Agent - DEV"
    page_icon: str = "🔧"
    layout: str = "wide"
    initial_sidebar_state: str = "expanded"

class Config:
    """Classe principal de configuração para desenvolvimento."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.openai = OpenAIConfig()
        self.rag = RagConfig()
        self.logging = LoggingConfig()
        self.streamlit = StreamlitConfig()
        
        self._load_secrets()
    
    def _load_secrets(self):
        """Carrega secrets e variáveis sensíveis."""
        self.openai.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai.api_key:
            raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    def get_database_path(self, connection_type: str) -> str:
        """Retorna o caminho do banco baseado no tipo de conexão."""
        from model.enum.connection_type import ConnectionType
        
        if ConnectionType(connection_type) in [
            ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, 
            ConnectionType.CONNECTION_WITH_SUMARY_MEMORY
        ]:
            return self.database.hp_path
        return self.database.tcc_path
    
    def get_file_path(self, connection_type: str) -> str:
        """Retorna o caminho do arquivo baseado no tipo de conexão."""
        from model.enum.connection_type import ConnectionType
        
        if ConnectionType(connection_type) in [
            ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, 
            ConnectionType.CONNECTION_WITH_SUMARY_MEMORY
        ]:
            return "files/harry-potter-1-cap-1.pdf"
        return "files/tcc.pdf"
    
    def validate(self):
        """Valida se todas as configurações obrigatórias estão presentes."""
        if not self.openai.api_key:
            raise ValueError("API Key da OpenAI é obrigatória")
        
        if not os.path.exists(self.database.tcc_path):
            print(f"Aviso: Caminho do banco TCC não encontrado: {self.database.tcc_path}")
        
        if not os.path.exists(self.database.hp_path):
            print(f"Aviso: Caminho do banco HP não encontrado: {self.database.hp_path}")


# Instância global de configuração
config = Config()


def get_config() -> Config:
    """Retorna a instância global de configuração."""
    return config 