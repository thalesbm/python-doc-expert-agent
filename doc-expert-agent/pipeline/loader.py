from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_core.documents import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

from typing import List
from PyPDF2 import PdfReader

import io
import logging

logger = logging.getLogger(__name__)

class Loader:

    def load_document(file: UploadedFile) -> List[Document]:
        logger.info("Iniciando carregando do documento...")

        documents = []

        if file is None:
            logger.info("Não foi encontrado arquivo anexado")

            file_path = "files/tcc.pdf"
            
            try:
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            except Exception as e:
                print(f"Erro ao carregar PDF: {e}")
                raise

        else:
            logger.info("Foi encontrado arquivo anexado")

            try:
                file_bytes = file.read()
                pdf_reader = PdfReader(io.BytesIO(file_bytes))
                documents = []
                for i, page in enumerate(pdf_reader.pages):
                    text = page.extract_text() or ""
                    documents.append(Document(page_content=text, metadata={"page": i + 1}))
            except Exception as e:
                print(f"Erro ao carregar PDF: {e}")
                raise
            
        logger.info("Finalizando carregando do documento")

        return documents

