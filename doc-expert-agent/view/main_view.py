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
        
        with st.container():
            
            prompt_type_option = None

            connection_type_option = MainView.get_connection_type()

            if connection_type_option == "conexao-simples-llm":
                prompt_type_option, pergunta = MainView.render_conexao_simples_llm()
            
            elif connection_type_option in ["conexao-llm-complete-memory", "conexao-llm-summary-memory"]:
                pergunta = MainView.render_conexao_memory_llm()
                
            elif connection_type_option in ["conexao-com-tool", "conexao-com-tool-react"]:
                pergunta = MainView.render_conexao_tools_llm()
            
            with st.form(key="meu_formulario"):
                # Campo de pergunta
                question_input = st.text_area(
                    "Digite sua pergunta:",
                    value=pergunta,
                    height=60,
                )
                
                # Botão de envio
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    submit = st.form_submit_button(
                        "Enviar Pergunta",
                        use_container_width=True
                    )

            if submit:
                if question_input and question_input.strip():
                    input = Input(
                        question=question_input,
                        connection_type=connection_type_option,
                        prompt_type=prompt_type_option
                    )
                    callback(input)
                else:
                    st.error("❌ Por favor, insira uma pergunta antes de enviar.")

    def get_connection_type():
        """Seletor de tipo de conexão."""
        return st.selectbox(
            "Escolha o tipo de conexão:",
            [
                "conexao-simples-llm", 
                "conexao-llm-complete-memory",
                "conexao-llm-summary-memory",
                "conexao-com-tool", 
                "conexao-com-tool-react", 
            ],
            format_func=lambda x: {
                "conexao-simples-llm": "Conexão Simples",
                "conexao-llm-complete-memory": "Memória Completa",
                "conexao-llm-summary-memory": "Memória Resumida",
                "conexao-com-tool": "Com Tools",
                "conexao-com-tool-react": "ReAct"
            }.get(x, x)
        )

    @staticmethod
    def render_conexao_simples_llm():
        """Renderiza interface para conexão simples."""

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

        st.info("**Observação:**\n- **Documento anexado:** TCC")
        pergunta = "quem escreveu o trabalho?"
        return prompt_type_option, pergunta

    @staticmethod
    def render_conexao_memory_llm():
        """Renderiza interface para conexão com memória."""
        st.info("**Observação:**\n- **Memória Completa:** Mantém todo o histórico da conversa\n- **Memória Resumida:** Cria resumos automáticos da conversa \n- **Documento anexado:** Livro do Harry Potter e a Pedra Filosofal, capítulo 1")
        pergunta = "Sempre que eu perguntar qual o meu nome, voce responde: Thales. Resume o livro em 15 palavras."
        return pergunta

    @staticmethod
    def render_conexao_tools_llm():
        """Renderiza interface para conexão com tools."""        
        st.info("**Observação:**\n- **celulares_atualizados():** Retorna quantidade de celulares no Brasil\n- O sistema detecta automaticamente quando usar ferramentas \n- **Documento anexado:** TCC")
        pergunta = "Quantos celulares o app pode rodar em 2025?"
        return pergunta


    @staticmethod
    def update_view_with_chunks(answers: List[Answer]):
        """Atualiza a view com os chunks recuperados."""
        st.subheader("🧩 Chunks Recuperados")
        
        if not answers:
            st.warning("⚠️ Nenhum chunk foi encontrado para a pergunta.")
            return
        
        for i, answer in enumerate(answers, 1):
            with st.expander(f"📄 Chunk {i}", expanded=False):
                st.write("**Conteúdo:**")
                st.write(answer.content)
                
                if answer.metadata:
                    st.write("**Metadados:**")
                    st.write(answer.metadata)

    @staticmethod
    def update_view_with_result(result: str):
        """Atualiza a view com o resultado final."""
        st.subheader("✅ Resposta Final")
        st.write(result)

    @staticmethod
    def update_view_with_evaluate(evaluate: str):
        """Atualiza a view com a avaliação."""
        st.subheader("🔍 Avaliação de Qualidade")
        st.write(evaluate)
