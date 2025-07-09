from controller.main_controller import MainController
from view.main_view import MainView

import streamlit as st
import logging

logger = logging.getLogger(__name__)

def init():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    logger.info("Bem vindo ao melhor mini agente do mundo")

    MainView.set_view(get_form)
    
def get_form(
        question: str, 
        connection_type_option: str, 
        prompt_type_option: str,
    ):

    if "controller" not in st.session_state:
        st.session_state.controller = MainController()
        logger.info("Controller inicializado!")

    if question:
        evaluate = st.session_state.controller.run(
            connection_type_option=connection_type_option,
            prompt_type_option=prompt_type_option,
            question=question, 
            chunks_callback=MainView.update_view_with_chunks,
            result_callback=MainView.update_view_with_result
        )
        MainView.update_view_with_evaluate(evaluate)

if __name__ == "__main__":
    init()
