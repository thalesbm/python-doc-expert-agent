from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document

from model.enum.connection_type import ConnectionType
from logger import get_logger
from config.config import get_config

from typing import List

logger = get_logger(__name__)

class Loader:
    """Classe responsável por carregar documentos PDF."""

    def load_document(connection_type: str) -> List[Document]:
        logger.info("Iniciando carregando do documento...")

        config = get_config()
        documents = []

        if ConnectionType(connection_type) in [
            ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, 
            ConnectionType.CONNECTION_WITH_SUMARY_MEMORY
        ]:
            file_path = config.path.hp_path
            logger.info("Selecionado livro do HP")
        else:
            file_path = config.path.tcc_path
            logger.info("Selecionado TCC")

        logger.info(f"Carregando arquivo: {file_path}")
        
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        except Exception as e:
            logger.error(f"Erro ao carregar PDF: {e}")
            raise
            
        logger.info("Finalizando carregando do documento")

        return documents

