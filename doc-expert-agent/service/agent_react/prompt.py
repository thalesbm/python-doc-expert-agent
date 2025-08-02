from typing import Any
from langchain.prompts import ChatPromptTemplate

class Prompt:
    """Classe responsável por gerar prompts para o agente ReAct."""

    @staticmethod
    def get_react_prompt() -> ChatPromptTemplate:
        prompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você é um assistente que universitario que retorna as informações de forma clara e objetiva"
                "Sempre explique seu raciocínio (Thought), execute uma ação (Action) e observe o resultado (Observation) e, quando já tiver a resposta final, escreva exatamente:"
                "Final Answer: <sua resposta aqui> "
                "Quando usar uma ferramenta (tool), utilize a observação (Observation) para compor a resposta final. "
                "Se a ferramenta já respondeu à pergunta, escreva 'Final Answer:' seguido da resposta, e NÃO chame mais nenhuma tool. "
                "Nunca repita chamadas desnecessárias. "
                "Contexto: {context}\n"
                "{agent_scratchpad}"
            ),
            (
                "user", 
                "Quantos celulares o aplicativo pode rodar em 2025?"),
            (
                "assistant",
                "Thought: Preciso consultar a função celulares_atualizados para obter a quantidade de celulares.\n"
                "Action: celulares_atualizados()\n"
                "Observation: 20.000\n"
                "Thought: Já tenho a informação necessária.\n"
                "Final Answer: O aplicativo pode rodar em 20.000 celulares diferentes em 2025."
            ),
            (   
                "user", 
                "Qual foi o objetivo do seu TCC?"
            ),
            (
                "assistant", 
                "O objetivo do meu TCC foi desenvolver um app para ensino de física."
            ),
            (
                "user", 
                "Que plataforma foi usada para o desenvolvimento?"
            ),
            (
                "assistant", 
                "Utilizei a plataforma Intel XDK."
            ),
            (
                "user", 
                "Qual foi o ano que o projeto foi apresentado?"
            ),
            (
                "assistant", 
                "O ano foi 2014."
            ),
            (
                "user", 
                "Pergunta: \n{query}"
            )
        ])
        return prompt
    