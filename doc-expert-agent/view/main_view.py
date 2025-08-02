from model.answer import Answer
from model.input import Input
import streamlit as st

from typing import List

from logger import get_logger

logger = get_logger(__name__)

class MainView:
    """Classe responsável pela interface de usuário usando Streamlit."""

    @staticmethod
    def set_view(callback):
        logger.info("Configurando View")
        
        st.subheader("Escolha as configurações abaixo e faça a sua pergunta")
        
        prompt_type_option = None
        question = None

        connection_type_option = MainView.get_connection_typpe()

        if connection_type_option == "conexao-simples-llm":
            prompt_type_option, question = MainView.render_conexao_simples_llm()
        
        elif connection_type_option in ["conexao-llm-complete-memory", "conexao-llm-summary-memory"]:
            question = MainView.render_conexao_memory_llm()
            
        elif connection_type_option in ["conexao-com-tool", "conexao-com-tool-react"]:
            question = MainView.render_conexao_tools_llm()

        with st.form(key="meu_formulario"):
            submit = st.form_submit_button(label="Enviar")

        if submit:
            input = Input(
                question=question,
                connection_type=connection_type_option,
                prompt_type=prompt_type_option
            )
            callback(input)

    def get_connection_typpe():
        connetion_type_option = st.selectbox("Tipo de Conexão",
            [
                "conexao-simples-llm", 
                "conexao-llm-complete-memory",
                "conexao-llm-summary-memory",
                "conexao-com-tool", 
                "conexao-com-tool-react", 
                
            ],
            format_func=lambda x: {
                "conexao-simples-llm": "Simples",
                "conexao-llm-complete-memory": "Memória Completa",
                "conexao-llm-summary-memory": "Memória com Resumo Automático",
                "conexao-com-tool": "Com Tool",
                "conexao-com-tool-react": "Com Tool e ReAct",
            }.get(x, x)
        )

        return connetion_type_option
        

    @staticmethod
    def render_conexao_simples_llm():
        prompt_type_option = st.selectbox(
            "Tipo de Prompt:",
            [   
                "ZERO_SHOT_PROMPT", 
                "FEW_SHOT_PROMPT", 
                "CHAIN_OF_THOUGHT", 
                "DEFINITION_EXEMPLIFICATION",
                "STYLE_SPECIFIC_PROMPTING", 
                "LENGHT_LIMITATION_PROMPTING", 
                "STEP_BY_STEP_INSTRUCTION_PROMPTING",
            ],
            format_func=lambda x: {
                "ZERO_SHOT_PROMPT": "Zero Shot",
                "FEW_SHOT_PROMPT": "Few Shot",
                "CHAIN_OF_THOUGHT": "Chain of Thought",
                "DEFINITION_EXEMPLIFICATION": "Definição + Exemplo",
                "STYLE_SPECIFIC_PROMPTING": "Estilo Específico",
                "LENGHT_LIMITATION_PROMPTING": "Limitação de Tamanho",
                "STEP_BY_STEP_INSTRUCTION_PROMPTING": "Passo a Passo"
            }.get(x, x)
        )
        question = st.text_input(
            "Faça sua pergunta sobre o TCC da minha faculdade", 
            value = "quem escreveu o trabalho?"
        )

        with st.sidebar:
            st.title("Observações")
            st.write("Escolha o tipo de prompt que deseja usar")

        return prompt_type_option, question

    @staticmethod
    def render_conexao_memory_llm():
        question = st.text_input(
            "Faça sua pergunta sobre o primeiro capitulo do livro Harry Potter e a Pedra Filosofal", 
            value = "Sempre que eu perguntar qual o meu nome, voce responde: Thales. Resume o livro em 15 palavras."
        )

        with st.sidebar:
            st.title("Observações")
            st.write("Utilizando memória de histórico completa: (ConversationBufferMemory)")
            st.write("Utilizando memória com resumo automático: (ConversationSummaryMemory)")

        return question

    @staticmethod
    def render_conexao_tools_llm():
        question = st.text_input(
            "Faça sua pergunta sobre o TCC da minha faculdade", 
            value = "Quantos celulares o app pode rodar em 2025?"
        )

        with st.sidebar:
            st.title("Observações")
            st.write("Esse tipo de conexão chama uma tool caso o LLM identifique que o usuário fez alguma perguntou relacionada a quantidade de celulares disponivel no Brasil")
           
        return question

    @staticmethod
    def update_view_with_chunks(answers: List[Answer]):
        st.subheader("🧩 Chunks recuperados:")
        
        for answer in answers:
            st.write(answer.content)

    @staticmethod
    def update_view_with_result(result: str):
        st.subheader("✅ Resposta final OpenAI:")
        st.write(result)

    @staticmethod
    def update_view_with_evaluate(evaluate: str):
        st.subheader("🔍 Avaliação:")
        st.write(evaluate)
