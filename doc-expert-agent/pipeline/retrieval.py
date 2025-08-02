import asyncio
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from model.answer import Answer
from logger import get_logger
from config.config import get_config
from typing import List

logger = get_logger(__name__)

class Retrieval:
    """Classe responsável por recuperar documentos similares do banco vetorial."""

    def __init__(self):
        pass

    async def retrieve_similar_documents(self, question: str, api_key: str, database_path: str) -> List[Answer]: 
        """Recupera documentos similares de forma assíncrona."""
        logger.info("Iniciando retrieval do documento...")

        config = get_config()
        vector_store = await self.get_vector_store_async(api_key=api_key, database_path=database_path)
        
        # Realizar busca de forma assíncrona
        docs = await self._search_documents_async(
            vector_store=vector_store,
            question=question,
            config=config
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

    async def get_vector_store_async(self, api_key: str, database_path: str) -> Chroma:
        """Obtém vector store de forma assíncrona."""
        # Verificar se o banco existe de forma assíncrona
        if not await self._database_exists_async(database_path):
            logger.error(f"O banco vetorial {database_path} não existe. Rode o indexador primeiro!")
            raise FileNotFoundError(f"Banco vetorial não encontrado: {database_path}")

        # Criar vector store de forma assíncrona
        return await self._create_vector_store_async(api_key, database_path)

    async def _database_exists_async(self, database_path: str) -> bool:
        """Verifica se o banco existe de forma assíncrona."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, os.path.exists, database_path)

    async def _create_vector_store_async(self, api_key: str, database_path: str) -> Chroma:
        """Cria vector store de forma assíncrona."""
        loop = asyncio.get_event_loop()
        
        def _create_vector_store_sync():
            return Chroma(
                embedding_function=OpenAIEmbeddings(api_key=api_key),
                persist_directory=database_path
            )
        
        return await loop.run_in_executor(None, _create_vector_store_sync)

    async def _search_documents_async(self, vector_store: Chroma, question: str, config) -> List:
        """Realiza busca de documentos de forma assíncrona."""
        loop = asyncio.get_event_loop()
        
        def _search_documents_sync():
            return vector_store.max_marginal_relevance_search(
                query=question,
                k=config.rag.top_k,
                fetch_k=config.rag.fetch_k,
                score_threshold=config.rag.score_threshold,
            )
        
        return await loop.run_in_executor(None, _search_documents_sync)

    def retrieve_similar_documents_sync(self, question: str, api_key: str, database_path: str) -> List[Answer]:
        """Versão síncrona para compatibilidade."""
        return asyncio.run(self.retrieve_similar_documents(question, api_key, database_path))
    
    def get_vector_store(self, api_key: str, database_path: str):
        """Versão síncrona para compatibilidade."""
        if not os.path.exists(database_path):
            logger.error(f"O banco vetorial {database_path} não existe. Rode o indexador primeiro!")

        vector_store = Chroma(
            embedding_function=OpenAIEmbeddings(api_key=api_key),
            persist_directory=database_path
        )
        return vector_store
