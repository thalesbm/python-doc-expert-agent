from langchain.prompts import ChatPromptTemplate

class Prompt:

    def get_entry_prompt():
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você é um assistente universitário. Responda com bastante detalhes"
                "Se o usuário perguntar sobre a quantidade de celulares em que o aplicativo pode rodar, "
                "OBRIGATORIAMENTE chame a função celulares_atualizados(). "
                "NUNCA tente responder com conhecimento próprio, só use a função celulares_atualizados(). "
                "Sempre priorize o uso de tools quando disponível. "
                "Contexto: {context}\n"
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

    def get_exit_prompt() -> str:
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "Você é um assistente que reescreve a resposta final de forma NATURAL, "
                "unindo o texto original e o valor da função. "
                "NÃO diga que chamou uma função. "
                "Apenas escreva o resultado como se fosse informação que você mesmo sabe."
            ),
            (
                "user",
                "Texto original: {resposta}\n"
                "Valor da função: {valor}\n"
                "Reescreva tudo de forma clara e natural, sem mencionar funções."
            )
        ])

        return prompt
