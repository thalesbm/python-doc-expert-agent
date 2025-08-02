from dataclasses import dataclass

@dataclass
class Answer:
    """Classe que representa a resposta gerada pelo sistema."""
    content: str
    metadata: str
