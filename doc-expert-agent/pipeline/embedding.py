import asyncio
import shutil
import os
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from typing import List
from logger import get_logger

logger = get_logger(__name__)

class Embedding:
    """Classe responsável por realizar o embedding."""

    @staticmethod
    def embedding_document_sync(chunks: List[Document], api_key: str, path: str) -> Chroma:
        """Versão síncrona para compatibilidade."""
        return asyncio.run(Embedding.embedding_document(chunks, api_key, path))

    @staticmethod
    async def embedding_document(chunks: List[Document], api_key: str, path: str) -> Chroma:
        """Realiza embedding do documento de forma assíncrona."""
        logger.info("Inicializando embedding do documento...")

        if not chunks:
            logger.warning("Lista de chunks vazia para embedding.")
            return None

        # Criar embeddings de forma assíncrona
        embeddings = await Embedding._create_embeddings_async(api_key)
        
        logger.info("Iniciando análise")

        # Criar vector store de forma assíncrona
        vector_store = await Embedding._create_vector_store_async(
            documents=chunks,
            embedding=embeddings,
            persist_directory=path
        )

        logger.info("Persistindo no db")

        # Persistir de forma assíncrona
        await Embedding._persist_vector_store_async(vector_store)

        logger.info("Finalizando embedding do documento")

        return vector_store

    @staticmethod
    async def _create_embeddings_async(api_key: str) -> OpenAIEmbeddings:
        """Cria embeddings de forma assíncrona."""
        loop = asyncio.get_event_loop()
        
        def _create_embeddings_sync():
            return OpenAIEmbeddings(openai_api_key=api_key)
        
        return await loop.run_in_executor(None, _create_embeddings_sync)

    @staticmethod
    async def _create_vector_store_async(documents: List[Document], embedding: OpenAIEmbeddings, persist_directory: str) -> Chroma:
        """Cria vector store de forma assíncrona."""
        loop = asyncio.get_event_loop()
        
        def _create_vector_store_sync():
            return Chroma.from_documents(
                documents=documents,
                embedding=embedding,
                persist_directory=persist_directory
            )
        
        return await loop.run_in_executor(None, _create_vector_store_sync)

    @staticmethod
    async def _persist_vector_store_async(vector_store: Chroma):
        """Persiste vector store de forma assíncrona."""
        loop = asyncio.get_event_loop()
        
        def _persist_sync():
            vector_store.persist()
        
        await loop.run_in_executor(None, _persist_sync)

@staticmethod
async def clean_path(path: str):
    """Limpa o diretório de forma assíncrona."""
    loop = asyncio.get_event_loop()
    
    def _clean_path_sync():
        if os.path.exists(path):
            logger.info("Removendo db")
            shutil.rmtree(path)

        if not os.path.exists(path):
            logger.info("Path foi removido com sucesso")
        else:
            logger.info("Path ainda existe")    
        
        os.makedirs(path)
    
    await loop.run_in_executor(None, _clean_path_sync)

def clean_path_sync(path: str):
    """Versão síncrona para compatibilidade."""
    return asyncio.run(clean_path(path))
