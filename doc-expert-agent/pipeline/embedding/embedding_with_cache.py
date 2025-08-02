"""
Versão completa do embedding com cache real implementado.
"""

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from typing import List, Dict, Any
from logger import get_logger
from pathlib import Path
from .embedding_cache import EmbeddingCache
import numpy as np

logger = get_logger(__name__)


class EmbeddingWithCache:
    """Classe de embedding com cache completo implementado."""

    def __init__(self, cache_dir: str = "files/cache/embeddings"):
        self.cache = EmbeddingCache(cache_dir, max_size_mb=1000)
        self.model = "text-embedding-ada-002"
        self.logger = get_logger(__name__)

    def embedding_document(self, chunks: List[Document], api_key: str, path: str) -> Chroma:
        """
        Processa documentos com cache de embeddings.
        
        Args:
            chunks: Lista de chunks para processar
            api_key: Chave da API OpenAI
            path: Caminho para salvar o vector store
            
        Returns:
            Vector store com embeddings
        """
        self.logger.info("Inicializando embedding do documento com cache...")

        if not chunks:
            self.logger.warning("Lista de chunks vazia para embedding.")
            return None

        # Separa chunks cacheados e não cacheados
        cached_embeddings = {}
        uncached_chunks = []
        
        for chunk in chunks:
            chunk_text = chunk.page_content
            
            if self.cache.is_cached(chunk_text, self.model):
                self.logger.info(f"Chunk encontrado no cache: {chunk_text[:50]}...")
                embedding = self.cache.get_from_cache(chunk_text, self.model)
                cached_embeddings[chunk_text] = embedding
            else:
                self.logger.info(f"Chunk não encontrado no cache: {chunk_text[:50]}...")
                uncached_chunks.append(chunk)

        self.logger.info(f"Chunks em cache: {len(cached_embeddings)}, Chunks para processar: {len(uncached_chunks)}")

        # Gera embeddings para chunks não cacheados
        new_embeddings = {}
        if uncached_chunks:
            new_embeddings = self._generate_embeddings_for_chunks(uncached_chunks, api_key)
            
            # Salva novos embeddings no cache
            for chunk in uncached_chunks:
                chunk_text = chunk.page_content
                if chunk_text in new_embeddings:
                    self.cache.save_to_cache(chunk_text, self.model, new_embeddings[chunk_text])
                    self.logger.info(f"Embedding salvo no cache: {chunk_text[:50]}...")

        # Combina todos os embeddings
        all_embeddings = {**cached_embeddings, **new_embeddings}
        
        # Cria vector store
        vector_store = self._create_vector_store(chunks, all_embeddings, path)
        
        # Obtém estatísticas do cache
        stats = self.cache.get_cache_stats()
        self.logger.info(f"Estatísticas do cache: {stats}")
        
        return vector_store

    def _generate_embeddings_for_chunks(self, chunks: List[Document], api_key: str) -> Dict[str, List[float]]:
        """
        Gera embeddings para chunks usando OpenAI.
        
        Args:
            chunks: Lista de chunks
            api_key: Chave da API
            
        Returns:
            Dicionário com embeddings
        """
        embeddings_model = OpenAIEmbeddings(openai_api_key=api_key)
        embeddings_dict = {}
        
        self.logger.info(f"Gerando embeddings para {len(chunks)} chunks...")
        
        for chunk in chunks:
            try:
                chunk_text = chunk.page_content
                embedding = embeddings_model.embed_query(chunk_text)
                embeddings_dict[chunk_text] = embedding
                self.logger.info(f"Embedding gerado para: {chunk_text[:50]}...")
            except Exception as e:
                self.logger.error(f"Erro ao gerar embedding para chunk: {e}")
        
        return embeddings_dict

    def _create_vector_store(self, chunks: List[Document], embeddings: Dict[str, List[float]], path: str) -> Chroma:
        """
        Cria vector store com embeddings.
        
        Args:
            chunks: Lista de chunks
            embeddings: Dicionário de embeddings
            path: Caminho para salvar
            
        Returns:
            Vector store
        """
        self.logger.info("Criando vector store...")
        
        # Cria embeddings model customizado que usa cache
        class CachedEmbeddings:
            def __init__(self, embeddings_dict):
                self.embeddings_dict = embeddings_dict
            
            def embed_query(self, text):
                return self.embeddings_dict.get(text, [0.0] * 1536)  # Fallback
            
            def embed_documents(self, texts):
                return [self.embeddings_dict.get(text, [0.0] * 1536) for text in texts]

        cached_embeddings_model = CachedEmbeddings(embeddings)
        
        # Cria vector store
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=cached_embeddings_model,
            persist_directory=path
        )
        
        self.logger.info("Persistindo vector store...")
        vector_store.persist()
        
        self.logger.info("Vector store criado com sucesso!")
        return vector_store

    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas do cache."""
        return self.cache.get_cache_stats()

    def clear_cache(self):
        """Limpa o cache."""
        self.cache.clear_cache()
        self.logger.info("Cache limpo!") 