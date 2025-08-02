from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config.config import get_config
from .adaptive_chunker import AdaptiveChunker

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

        chunks = fixed_chunks(documents)
        # adaptive_chunks = self.adaptive_chunks(documents)

        # logger.info(f"Chunking fixo: {len(fixed_chunks)} chunks")
        # logger.info(f"Chunking adaptativo: {len(adaptive_chunks)} chunks")
        
        # # Compara tamanhos
        # fixed_lengths = [len(chunk.page_content) for chunk in fixed_chunks]
        # adaptive_lengths = [len(chunk.page_content) for chunk in adaptive_chunks]
        
        # logger.info(f"Tamanhos fixos: {fixed_lengths}")
        # logger.info(f"Tamanhos adaptativos: {adaptive_lengths}")

        return chunks

def fixed_chunks(documents: List[Document]) -> List[Document]:
    logger.info("Iniciando split do documento (fixed_chunks)...")

    config = get_config()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.rag.chunk_size,
        chunk_overlap=config.rag.chunk_overlap,
        separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", " "]
    )

    chunks = text_splitter.split_documents(documents)        
    unique_chunks = remove_duplicate_chunks(chunks)

    return unique_chunks

def adaptive_chunks(documents: List[Document]) -> List[Document]:
    logger.info("Iniciando split do documento (adaptive_chunks)...")
    
    adaptive_chunker = AdaptiveChunker()
    adaptive_chunks = adaptive_chunker.chunk_documents(documents)

    return adaptive_chunks

def remove_duplicate_chunks(chunks: List[Document]):
    unique_chunks = []
    seen_contents = set()

    for chunk in chunks:
        if chunk.page_content not in seen_contents:
            unique_chunks.append(chunk)
            seen_contents.add(chunk.page_content)
    return unique_chunks
