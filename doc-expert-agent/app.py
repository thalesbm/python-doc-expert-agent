from controller.main_controller import MainController
from view.main_view import MainView
from model.input import Input
from model.enum.connection_type import ConnectionType
from config import get_config
from infra import setup_logging, get_logger
from model.enum.database_path import DatabasePath

import streamlit as st

logger = get_logger(__name__)

def init():
    # Carrega configuração
    config = get_config()
    
    # Configura logging centralizado
    setup_logging(
        level=config.logging.level,
        format_string=config.logging.format,
        log_file=config.logging.file_path
    )
    
    # Configura Streamlit
    st.set_page_config(
        page_title=config.streamlit.page_title,
        page_icon=config.streamlit.page_icon,
        layout=config.streamlit.layout,
        initial_sidebar_state=config.streamlit.initial_sidebar_state
    )
    
    logger.info("Bem vindo ao melhor mini agente do mundo")

    MainView.set_view(get_form)
    
def get_form(input: Input):

    controller = None

    if ConnectionType(input.connection_type) in [ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, ConnectionType.CONNECTION_WITH_SUMARY_MEMORY]:
        logger.info("View: Memory")
        if "controller_memory" not in st.session_state:
            st.session_state.controller_memory = MainController(connection_type=input.connection_type, database_path=DatabasePath.HP_PATH)
            logger.info("controller_memory inicializado!")
        
        if input.question:
            controller = st.session_state.controller_memory

    else:
        if "controller_default" not in st.session_state:
            logger.info("View: Others")
            st.session_state.controller_default = MainController(connection_type=input.connection_type, database_path=DatabasePath.TCC_PATH)
            logger.info("controller_default inicializado!")

        if input.question:
            controller = st.session_state.controller_default
    
    evaluate = controller.run(
        input=input,
        chunks_callback=MainView.update_view_with_chunks,
        result_callback=MainView.update_view_with_result
    )
    MainView.update_view_with_evaluate(evaluate)

if __name__ == "__main__":
    init()
