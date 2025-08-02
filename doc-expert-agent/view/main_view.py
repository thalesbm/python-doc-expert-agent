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
        return st.selectbox("🔌 Tipo de Conexão",
            [
                "conexao-simples-llm", 
                "conexao-llm-complete-memory",
                "conexao-llm-summary-memory",
                "conexao-com-tool", 
                "conexao-com-tool-react", 
                
            ]
        )

    @staticmethod
    def render_conexao_simples_llm():
        prompt_type_option = st.selectbox("🎯 Tipo de Prompt",
            [   
                "ZERO_SHOT_PROMPT", 
                "FEW_SHOT_PROMPT", 
                "CHAIN_OF_THOUGHT", 
                "DEFINITION_EXEMPLIFICATION",
                "STYLE_SPECIFIC_PROMPTING", 
                "LENGHT_LIMITATION_PROMPTING", 
                "STEP_BY_STEP_INSTRUCTION_PROMPTING",
            ]
        )
        question = st.text_input(
            "✏️ Faça sua pergunta sobre o TCC da minha faculdade", 
            value = "quem escreveu o trabalho?"
        )

        return prompt_type_option, question

    @staticmethod
    def render_conexao_memory_llm():
        question = st.text_input(
            "✏️ Faça sua pergunta sobre o primeiro capitulo do livro Harry Potter e a Pedra Filosofal", 
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
            "✏️ Faça sua pergunta sobre o TCC da minha faculdade", 
            value = "Quantos celulares o app pode rodar em 2025?"
        )

        with st.sidebar:
            st.title("Observações")
            st.write("Esse tipo de conexão chama uma tool caso o LLM identifique que o usuário fez alguma perguntou relacionada a quantidade de celulares disponivel no Brasil")
           
        return question

    @staticmethod
    def display_side_bar():
        with st.sidebar:
            st.title("📄 Documentos")
            st.write("Caso não anexe um arquivo, usaremos o padrão: `doc-expert-agent/files/tcc.pdf`")

            st.write("Na pasta `doc-expert-agent/files/` tem alguns arquivos em pdf para anexar")
            return st.file_uploader(
                key="file-pdf",
                label="Anexar PDF",
                type="pdf",
                accept_multiple_files=False,
            )
        return None

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
