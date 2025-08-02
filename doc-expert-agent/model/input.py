from dataclasses import dataclass

@dataclass
class Input:
    """Classe que representa a entrada de dados do usuário."""
    question: str
    connection_type: str
    prompt_type: str
