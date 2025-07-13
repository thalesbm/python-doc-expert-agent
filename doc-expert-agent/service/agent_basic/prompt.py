from langchain.schema import HumanMessage, SystemMessage, AIMessage

class Prompt:

    def __init__(self, question: str, context: str):
        self.question = question
        self.context = context

    def default_prompt(self): 
        prompt = [
            SystemMessage(content="Você é um aluno universitario que escreveu um TCC"),
            HumanMessage(content=f"Se baseia APENAS no contexto para sua resposta: \n{self.context}"),
            HumanMessage(content=f"Responda a pergunta de forma clara e objetiva: \n{self.question}"),
            HumanMessage(content=("Não invente respostas. ")),
        ]

        return prompt

    def get_zero_show_prompt(self):
        return self.default_prompt()
    
    def get_chain_of_thought(self):
        prompt = self.default_prompt()
        prompt.append(HumanMessage(content=("Responda em qual página ou páginas em caso de mais de uma você se baseou pra responder essa pergunta")))
        return prompt
    
    def get_lenght_limitation_prompting(self):
        prompt = self.default_prompt()
        prompt.append(HumanMessage(content=f"Responda utilizando no maximo 180 caracteres"))
        return prompt

    def get_style_specific_prompting(self):
        prompt = self.default_prompt()
        prompt.append(HumanMessage(content=f"Responda de forma ironica e com muito sarcasmo"))
        return prompt

    def get_few_show_prompt(self):
        prompt = [
            SystemMessage(content="Você é um aluno universitario que escreveu um TCC"),

            HumanMessage(content="Qual foi o objetivo do seu TCC? "),
            AIMessage(content="O objetivo do meu TCC foi desenvolver um app para ensino de física. "),

            HumanMessage(content="Que plataforma foi usada para o desenvolvimento? "),
            AIMessage(content="Utilizei a plataforma Intel XDK. "),

            HumanMessage(content="Qual foi o ano que o projeto foi apresentado? "),
            AIMessage(content="O ano foi 2014. "),

            HumanMessage(content=f"Se baseia APENAS no contexto para sua resposta: \n{self.context}"),
            HumanMessage(content=f"Pergunta: \n{self.question}"),
        ]

        return prompt

    def step_by_step_instruction_prompting(self):
        prompt = self.default_prompt()
        prompt.append(HumanMessage(content=("Siga estas etapas para responder:")))
        prompt.append(HumanMessage(content=("1. Analise o contexto e identifique as informações principais.")))
        prompt.append(HumanMessage(content=("2. Relacione essas informações com a pergunta.")))
        prompt.append(HumanMessage(content=("3. Explique a ligação entre contexto e resposta.")))
        return prompt

    def get_definition_exemplification(self):
        prompt = self.default_prompt()
        prompt.append(HumanMessage(content=("Em seguida, faça uma piada sore fisica")))
        return prompt
