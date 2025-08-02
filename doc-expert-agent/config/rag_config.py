from dataclasses import dataclass, field

@dataclass
class RagConfig:
    """Configurações do sistema RAG."""
    retrieval_strategy: int = 10
    max_context_length: int = 2000
    enable_evaluation: bool = True
    chunk_size: int = 1024
    chunk_overlap: int = 150
    top_k: int = 5 
    fetch_k: int = 20
    score_threshold: float = 0.85
    separator: list = field(default_factory=lambda: ["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", " "])