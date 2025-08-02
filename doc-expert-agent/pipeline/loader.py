from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document

from model.enum.connection_type import ConnectionType
from infra import get_logger

from typing import List

logger = get_logger(__name__)

class Loader:

    def load_document(connection_type: str) -> List[Document]:
        logger.info("Iniciando carregando do documento...")

        config = get_config()
        documents = []

        file_path = config.get_file_path(connection_type)
        logger.info(f"Carregando arquivo: {file_path}")
        
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        except Exception as e:
            logger.error(f"Erro ao carregar PDF: {e}")
            raise
            
        logger.info("Finalizando carregando do documento")

        return documents

