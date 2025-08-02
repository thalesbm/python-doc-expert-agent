"""
Exemplo de uso das melhorias de RAG:
- Chunking adaptativo
- Filtros de relevância
- Cache de embeddings
"""

from pipeline import AdaptiveChunker, RelevanceFilter, EmbeddingCache
from pipeline import Loader
from langchain_core.documents import Document
from logger import get_logger

logger = get_logger(__name__)


def example_adaptive_chunking():
    """Exemplo de uso do chunking adaptativo."""
    logger.info("=== Exemplo: Chunking Adaptativo ===")
    
    # Cria o chunker adaptativo
    chunker = AdaptiveChunker(base_chunk_size=512, base_overlap=100)
    
    # Carrega documentos
    documents = Loader.load_document("conexao-simples-llm")
    
    # Faz chunking adaptativo
    chunks = chunker.chunk_documents(documents)
    
    # Obtém estatísticas
    stats = chunker.get_chunk_stats(chunks)
    
    logger.info(f"Estatísticas dos chunks: {stats}")
    
    return chunks


def example_relevance_filtering(chunks):
    """Exemplo de uso dos filtros de relevância."""
    logger.info("=== Exemplo: Filtros de Relevância ===")
    
    # Cria o filtro de relevância
    relevance_filter = RelevanceFilter()
    
    # Aplica filtros padrão
    filtered_chunks = relevance_filter.apply_filters(chunks)
    
    # Obtém estatísticas
    stats = relevance_filter.get_filter_stats(chunks, filtered_chunks)
    
    logger.info(f"Estatísticas dos filtros: {stats}")
    
    # Exemplo de filtro personalizado por palavras-chave
    keywords = ["TCC", "projeto", "desenvolvimento"]
    keyword_filtered = [
        chunk for chunk in filtered_chunks 
        if relevance_filter.filter_by_keywords(chunk, keywords, min_matches=1)
    ]
    
    logger.info(f"Chunks com palavras-chave: {len(keyword_filtered)}")
    
    return filtered_chunks


def example_embedding_cache():
    """Exemplo de uso do cache de embeddings."""
    logger.info("=== Exemplo: Cache de Embeddings ===")
    
    # Cria o cache de embeddings
    cache = EmbeddingCache(cache_dir="cache/embeddings", max_size_mb=100)
    
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
        embedding = [0.1] * 1536  # Dimensão típica do Ada
        cache.save_to_cache(sample_text, model, embedding)
    
    # Obtém estatísticas do cache
    stats = cache.get_cache_stats()
    logger.info(f"Estatísticas do cache: {stats}")
    
    return cache


def main():
    """Função principal do exemplo."""
    logger.info("Iniciando exemplo das melhorias de RAG")
    
    try:
        # 1. Chunking adaptativo
        chunks = example_adaptive_chunking()
        
        # 2. Filtros de relevância
        filtered_chunks = example_relevance_filtering(chunks)
        
        # 3. Cache de embeddings
        cache = example_embedding_cache()
        
        logger.info("=== Resumo das Melhorias ===")
        logger.info(f"Chunks originais: {len(chunks)}")
        logger.info(f"Chunks após filtros: {len(filtered_chunks)}")
        logger.info("Cache configurado e funcionando")
        
        logger.info("Exemplo concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro no exemplo: {e}")


if __name__ == "__main__":
    main() 