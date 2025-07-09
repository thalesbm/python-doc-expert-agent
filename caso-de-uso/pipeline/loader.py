from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document

from typing import List
from functools import lru_cache

import logging

logger = logging.getLogger(__name__)

class Loader:

    @lru_cache(maxsize=1)
    def load_document() -> List[Document]:
        logger.info("Iniciando carregando do documento...")

        file_path = "files/tcc.pdf"
        
        try:
            loader = PyPDFLoader(file_path)
            document = loader.load()
        except Exception as e:
            print(f"Erro ao carregar PDF: {e}")
            raise

        logger.info("Finalizando carregando do documento")

        return document

