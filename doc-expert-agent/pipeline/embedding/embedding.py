from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma

from typing import List

from logger import get_logger
from pathlib import Path

from .embedding_cache import EmbeddingCache

logger = get_logger(__name__)

class Embedding:

    def __init__(self):
        pass

    def embedding_document(self, chunks: List[Document], api_key: str, path: str) -> Chroma:
        logger.info("Inicializando embedding do documento...")

        if not chunks:
            logger.warning("Lista de chunks vazia para embedding.")
            return None

        cache = EmbeddingCache(Path("files/cache/embeddings"), max_size_mb=100)
    
        # Exemplo de texto
        sample_text = "Este é um exemplo de texto para teste de cache de embeddings."
        model = "text-embedding-ada-002"
        
        # Verifica se está em cache
        if cache.is_cached(sample_text, model):
            logger.info("Embedding encontrado no cache!")
            embedding = cache.get_from_cache(sample_text, model)
        
        else:
            logger.info("Embedding não encontrado no cache, seria gerado aqui...")
            # Simula embedding (em uso real, seria gerado pela API)
            embedding = self.generate_embedding(chunks, api_key, path)
            
            cache.save_to_cache(sample_text, model, embedding)
        
        # Obtém estatísticas do cache
        stats = cache.get_cache_stats()
        logger.info(f"Estatísticas do cache: {stats}")
    
    def generate_embedding(self, chunks: List[Document], api_key: str, path: str) -> Chroma:
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

