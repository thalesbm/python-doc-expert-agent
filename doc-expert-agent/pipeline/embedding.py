from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from typing import List

import shutil
import logging
import os

logger = logging.getLogger(__name__)

class Embedding:

    def embedding_document(chunks: List[Document], api_key: str, path: str) -> Chroma:
        logger.info("Inicializando embedding do documento...")

        if not chunks:
            logger.warning("Lista de chunks vazia para embedding.")
            return None

        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        logger.info("Iniciando analise")

        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=path
        )

        logger.info("Persistindo no db")

        vector_store.persist()

        logger.info("Finalizando embedding do documento")

        return vector_store
    
def clean_path(path: str):
    if os.path.exists(path):
        logger.info("Removendo db")
        shutil.rmtree(path)

    if not os.path.exists(path):
        logger.info("Path foi removido com sucesso")
    else:
        logger.info("Path ainda existe")    
    
    os.makedirs(path)
