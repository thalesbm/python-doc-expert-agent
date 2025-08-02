from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document

from model.enum.connection_type import ConnectionType
from infra import get_logger

from typing import List

logger = get_logger(__name__)

class Loader:

    def load_document(connection_type: str) -> List[Document]:
        logger.info("Iniciando carregando do documento...")

        documents = []

        file_path = "files/tcc.pdf"
        if (ConnectionType(connection_type) in [ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, ConnectionType.CONNECTION_WITH_SUMARY_MEMORY]):
            file_path = "files/harry-potter-1-cap-1.pdf"
            logger.info("Selecionado livro do HP")
        
        try:
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        except Exception as e:
            print(f"Erro ao carregar PDF: {e}")
            raise
            
        logger.info("Finalizando carregando do documento")

        return documents

