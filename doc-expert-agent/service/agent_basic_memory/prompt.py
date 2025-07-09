from langchain.schema import HumanMessage, SystemMessage

class Prompt:

    def __init__(self, question: str, context: str):
        self.question = question
        self.context = context

    def default_prompt(self): 
        prompt = [
            SystemMessage(content="Você é amante de leitura que conhece os livros do Harry Potter como ninguem"),
            HumanMessage(content=f"Se baseia APENAS no contexto para sua resposta: \n{self.context}"),
            HumanMessage(content=f"Responda a pergunta de forma clara e objetiva: \n{self.question}")
        ]

        return prompt
