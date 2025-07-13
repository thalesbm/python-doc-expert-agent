from controller.main_controller import MainController
from view.main_view import MainView
from model.input import Input

import streamlit as st
import logging

logger = logging.getLogger(__name__)

def init():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    logger.info("Bem vindo ao melhor mini agente do mundo")

    MainView.set_view(get_form)
    
def get_form(input: Input):

    if "controller" not in st.session_state:
        st.session_state.controller = MainController(connection_type=input.connection_type)
        logger.info("Controller inicializado!")

    if input.question:
        evaluate = st.session_state.controller.run(
            input=input,
            chunks_callback=MainView.update_view_with_chunks,
            result_callback=MainView.update_view_with_result
        )
        MainView.update_view_with_evaluate(evaluate)

if __name__ == "__main__":
    init()
