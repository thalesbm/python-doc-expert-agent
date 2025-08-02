from typing import List
from langchain.schema import HumanMessage, SystemMessage, BaseMessage

class Prompt:
    """Classe responsável por gerar prompts para o agente com memória resumida."""

    def __init__(self, question: str, context: str, memory: str) -> None:
        self.question: str = question
        self.context: str = context
        self.memory: str = memory

    def default_prompt(self) -> List[BaseMessage]: 
        prompt: List[BaseMessage] = [
            SystemMessage(content="Você é amante de leitura que conhece os livros do Harry Potter como ninguem"),
            HumanMessage(content=f"Se baseia APENAS no contexto para sua resposta: \n{self.context}"),
            HumanMessage(content=f"Responda a pergunta de forma clara e objetiva: \n{self.question}"),
            HumanMessage(content=f"Memoria: \n{self.memory}")
        ]

        return prompt
