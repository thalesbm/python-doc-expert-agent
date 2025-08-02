from dataclasses import dataclass

@dataclass
class RagConfig:
    """Configurações do sistema RAG."""
    retrieval_strategy: int = 10
    max_context_length: int = 2000
    enable_evaluation: bool = True
    evaluation_metrics: list = None
    chunk_size: int = 1024
    chunk_overlap: int = 150
    top_k: int = 5 
    fetch_k: int = 20
    score_threshold: float = 0.85

    def __post_init__(self):
        if self.evaluation_metrics is None:
            self.evaluation_metrics = ["answer_relevancy", "faithfulness"]