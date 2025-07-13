from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from model.answer import Answer

from typing import List

import logging

logger = logging.getLogger(__name__)

class Retrieval:

    def retrieve_similar_documents(question: str, api_key: str) -> List[Answer]: 
        logger.info("Iniciando retrieval do documento...")

        docs = get_vector_store(api_key=api_key).max_marginal_relevance_search(question, k=5)

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
    
def get_vector_store(api_key: str):
    path = "./files/db"

    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(api_key=api_key),
        persist_directory=path
    )
    return vector_store
