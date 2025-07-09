from model.answer import Answer
import streamlit as st

from typing import List

import logging

logger = logging.getLogger(__name__)

class MainView():

    def set_view(callback):
        logging.info("Configurando View")
        
        st.header("📚 Perguntas sobre o seu TCC")
        st.subheader("Escolha as configurações abaixo e faça a sua pergunta")
        
        connection_type_option = st.selectbox("🔌 Tipo de Conexão",
            [
                "conexao-simples-llm", "conexao-com-tool", "conexao-com-tool-react"
            ]
        )

        prompt_type_option = None
        question = None

        if connection_type_option == "conexao-simples-llm":
            prompt_type_option = st.selectbox("🎯 Tipo de Prompt",
                [   
                    "ZERO_SHOT_PROMPT", "FEW_SHOT_PROMPT", "CHAIN_OF_THOUGHT", "DEFINITION_EXEMPLIFICATION",
                    "STYLE_SPECIFIC_PROMPTING", "LENGHT_LIMITATION_PROMPTING", "STEP_BY_STEP_INSTRUCTION_PROMPTING"
                ]
            )
            question = st.text_input("Digite sua pergunta", 
                                     value = "qual foi o aplicativo escolhido para o projeto?")
        
        elif connection_type_option in ["conexao-com-tool", "conexao-com-tool-react"]:
            question = st.text_input("✏️ Faça sua pergunta", 
                                     value = "Quantos celulares o app pode rodar em 2025?")  

        with st.form(key="meu_formulario"):
            submit = st.form_submit_button(label="Enviar")

        if submit:
            callback(question, connection_type_option, prompt_type_option)

    def update_view_with_chunks(answers: List[Answer]):
        st.subheader("Chunks recuperados:")
        
        for answer in answers:
            st.write(answer.content)

    def update_view_with_result(result: str):
        st.subheader("Resposta final OpenAI:")
        st.write(result)

    def update_view_with_evaluate(evaluate: str):
        st.subheader("Evaluate:")
        st.write(evaluate)