from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from logger import get_logger
from config.config import get_config
from .chunk_utils import remove_duplicate_chunks

logger = get_logger(__name__)

class FixedChunker:
    """Classe responsável por dividir documentos em chunks menores."""

    def __init__(self):
        pass

    def split_document(self,documents: List[Document]) -> List[Document]:
        logger.info("Iniciando split do documento (fixed_chunks)...")

        config = get_config()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.rag.chunk_size,
            chunk_overlap=config.rag.chunk_overlap,
            separators=config.rag.separator
        )

        chunks = text_splitter.split_documents(documents)        
        unique_chunks = remove_duplicate_chunks(chunks)

        return unique_chunks