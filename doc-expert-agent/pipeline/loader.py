import os
import asyncio
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document

from model.enum.connection_type import ConnectionType
from logger import get_logger
from config.config import get_config

from typing import List

logger = get_logger(__name__)

class Loader:
    """Classe responsável por carregar documentos PDF."""

    @staticmethod
    def load_document_sync(connection_type: str) -> List[Document]:
        """Versão síncrona para compatibilidade."""
        return asyncio.run(Loader.load_document(connection_type))

    @staticmethod
    async def load_document(connection_type: str) -> List[Document]:
        """Carrega documento PDF de forma assíncrona."""
        logger.info("Iniciando carregamento do documento...")

        config = get_config()
        documents = []

        if ConnectionType(connection_type) in [
            ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY, 
            ConnectionType.CONNECTION_WITH_SUMARY_MEMORY
        ]:
            file_path = config.path.hp_path
            logger.info("Selecionado livro do HP")
        else:
            file_path = config.path.tcc_path
            logger.info("Selecionado TCC")

        logger.info(f"Carregando arquivo: {file_path}")
        
        try:
            # Executar o carregamento em uma thread separada para não bloquear
            documents = await Loader._load_pdf_async(file_path)
            
            if not documents:
                logger.warning(f"PDF carregado mas sem conteúdo: {file_path}")

        except Exception as e:
            logger.error(f"Erro ao carregar PDF: {file_path} - {e}")
            raise Exception(f"Erro ao carregar PDF: {file_path} - {e}")
            
        logger.info(f"Documento carregado com sucesso: {len(documents)} páginas")
        return documents

    @staticmethod
    async def _load_pdf_async(file_path: str) -> List[Document]:
        """Carrega o PDF de forma assíncrona usando executor."""
        loop = asyncio.get_event_loop()
        
        def _load_pdf_sync():
            loader = PyPDFLoader(file_path)
            return loader.load()
        
        return await loop.run_in_executor(None, _load_pdf_sync)
