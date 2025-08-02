from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Configurações de banco de dados e RAG."""
    tcc_path: str = "files/tcc/chroma_db/"
    hp_path: str = "files/hp/chroma_db/"
