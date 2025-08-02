from langchain_core.documents import Document
from .chunk_adaptive import AdaptiveChunker
from .chunk_fixed import FixedChunker
from typing import List

from logger import get_logger

logger = get_logger(__name__)

class Splitter:
    """Classe responsável por dividir documentos em chunks menores."""

    def split_document(documents: List[Document]) -> List[Document]:
        if not documents:
            logger.warning("Nenhum documento recebido para split.")
            return []
        
        logger.info("Iniciando split do documento...")

        fixed_chunks = FixedChunker().split_document(documents)
        adaptive_chunks = AdaptiveChunker().chunk_documents(documents)

        logger.info(f"Chunking fixo: {len(fixed_chunks)} chunks")
        logger.info(f"Chunking adaptativo: {len(adaptive_chunks)} chunks")
        
        # Compara tamanhos
        fixed_lengths = [len(chunk.page_content) for chunk in fixed_chunks]
        adaptive_lengths = [len(chunk.page_content) for chunk in adaptive_chunks]
        
        logger.info(f"Tamanhos fixos: {fixed_lengths}")
        logger.info(f"Tamanhos adaptativos: {adaptive_lengths}")

        return adaptive_chunks
