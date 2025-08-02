from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from model.answer import Answer
from infra import get_logger

from typing import List

import os

logger = get_logger(__name__)

class Retrieval:

    def __init__(self):
        pass

    def retrieve_similar_documents(self, question: str, api_key: str, database_path: str) -> List[Answer]: 
        logger.info("Iniciando retrieval do documento...")

        config = get_config()
        vector_store = self.get_vector_store(api_key=api_key, database_path=database_path)
        docs = vector_store.max_marginal_relevance_search(
            query=question,
            k=config.database.top_k,
            fetch_k=config.database.fetch_k,
            score_threshold=config.database.score_threshold,
        )

        if not docs:
            logger.warning("Nenhum documento similar encontrado para a pergunta.")

        answers = []

        logger.info(f"Chunks size: {len(docs)}")

        for item in docs:
            if isinstance(item, tuple):
                doc = item[0]
            else:
                doc = item

            answers.append(Answer(content=doc.page_content, metadata=doc.metadata))
            logger.info(f"Retrieved chunk: {doc.page_content[:100]}... | Metadata: {doc.metadata}")

        logger.info("Finalizando retrieval do documento")

        return answers
    
    def get_vector_store(self, api_key: str, database_path: str):
        if not os.path.exists(database_path):
            logger.error(f"O banco vetorial {database_path} não existe. Rode o indexador primeiro!")

        vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(api_key=api_key),
            persist_directory=database_path
        )
        return vector_store
