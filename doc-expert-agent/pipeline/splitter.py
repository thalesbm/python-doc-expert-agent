from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from typing import List

import logging

logger = logging.getLogger(__name__)

class Splitter:
    def split_document(documents: List[Document]) -> List[Document]:
        logger.info("Iniciando split do documento...")

        if not documents:
            logger.warning("Nenhum documento recebido para split.")
            return []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150,
            separators=["\n\n", "\n", ". ", "? ", "! ", "; ", ": ", " "]
        )

        chunks = text_splitter.split_documents(documents)
        logger.info(f"Número de chunks gerados: {len(chunks)}")
        
        unique_chunks = remove_duplicate_chunks(chunks)
        logger.info(f"Número de chunks únicos: {len(unique_chunks)}")
        
        logger.info("Finalizando split do documento")

        return unique_chunks
    
def remove_duplicate_chunks(chunks: List[Document]):
    unique_chunks = []
    seen_contents = set()
    for chunk in chunks:
        if chunk.page_content not in seen_contents:
            unique_chunks.append(chunk)
            seen_contents.add(chunk.page_content)
    return unique_chunks