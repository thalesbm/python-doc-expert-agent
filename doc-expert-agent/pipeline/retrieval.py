from langchain_community.vectorstores.chroma import Chroma

from model.answer import Answer

from typing import List

import logging

logger = logging.getLogger(__name__)

class Retrieval:

    def retrieve_similar_documents(vector_store: Chroma, question: str) -> List[Answer]: 
        logger.info("Iniciando retrieval do documento...")

        docs = vector_store.max_marginal_relevance_search(question, k=5)

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
