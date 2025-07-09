from model.answer import Answer
from model.input import Input
import streamlit as st

from typing import List

import logging

logger = logging.getLogger(__name__)

class MainView:

    @staticmethod
    def set_view(callback):
        logging.info("Configurando View")
        
        st.subheader("Escolha as configurações abaixo e faça a sua pergunta")
        
        prompt_type_option = None
        question = None
        files = None

        connection_type_option = MainView.get_connection_typpe()

        if connection_type_option == "conexao-simples-llm":
            prompt_type_option, question, files = MainView.render_conexao_simples_llm()
        
        elif connection_type_option in ["conexao-simples-llm-memory"]:
            question, files = MainView.render_conexao_simples_memory_llm()
            
        elif connection_type_option in ["conexao-com-tool", "conexao-com-tool-react"]:
            question = MainView.render_conexao_tools_llm()

        with st.form(key="meu_formulario"):
            submit = st.form_submit_button(label="Enviar")

        if submit:
            input = Input(
                question=question,
                connection_type=connection_type_option,
                prompt_type=prompt_type_option,
                file=files
            )
            callback(input)

    def get_connection_typpe():
        return st.selectbox("🔌 Tipo de Conexão",
            [
                "conexao-simples-llm", 
                "conexao-simples-llm-memory",
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
            "✏️ Faça sua pergunta", 
            value = "qual foi o aplicativo escolhido para o projeto?"
        )
        
        files = MainView.display_side_bar()

        return prompt_type_option, question, files

    @staticmethod
    def render_conexao_simples_memory_llm():
        question = st.text_input(
            "✏️ Faça sua pergunta", 
            value = "Resume o documento anexado"
        )  
                
        files = MainView.display_side_bar()

        return question, files

    @staticmethod
    def render_conexao_tools_llm():
        question = st.text_input(
            "✏️ Faça sua pergunta", 
            value = "Quantos celulares o app pode rodar em 2025?"
        )
        return question

    @staticmethod
    def display_side_bar():
        with st.sidebar:
            st.title("📄 Documentos")
            st.write("Caso não anexe um arquivo, usaremos o padrão: `doc-expert-agent/files/tcc.pdf`")
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
