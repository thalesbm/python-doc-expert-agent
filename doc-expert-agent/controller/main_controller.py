import asyncio
from pipeline.loader import Loader
from pipeline.chunk.splitter import Splitter
from pipeline.embedding import Embedding
from pipeline.retrieval import Retrieval
from pipeline.openai import Key
from pipeline.evaluate import Evaluate

from service.select_service import SelectServices
from model.input import Input
from config.config import get_config
from logger import get_logger
from model.enum.database_path import DatabasePath

logger = get_logger(__name__)

class MainController:

    def __init__(self, connection_type: str, database_path: DatabasePath):
        logger.info("Iniciando setup do RAG...")

        self.database_path = database_path
        self.config = get_config()

        self.api_key = Key.get_openai_key()

        # Usar versão síncrona para compatibilidade no construtor
        document = Loader.load_document_sync(connection_type=connection_type)
        chunks = Splitter.split_document(document)
        
        Embedding.embedding_document_sync(chunks, self.api_key, database_path.value)

        logger.info("Setup do RAG finalizado!")

    async def run_async(
            self, 
            input: Input,
            chunks_callback, 
            result_callback
        ):        
        """Executa o pipeline RAG de forma assíncrona."""
        logger.info(f"Pergunta recebida: {input.question}")

        # retrieval assíncrono
        retrieval = Retrieval()
        chunks = await retrieval.retrieve_similar_documents(
            database_path=self.database_path.value,
            api_key=self.api_key,
            question=input.question
        )
        chunks_callback(chunks)

        # open ai (mantém síncrono por enquanto, pois SelectServices não é async)
        result = SelectServices(
            answers=chunks,
            api_key=self.api_key,
        ).run(
            input=input
        )
        result_callback(result)

        # evaluate (mantém síncrono por enquanto)
        evaluate = None
        if self.config.rag.enable_evaluation:
            evaluate = Evaluate(
                answer=result,
                chunks=chunks, 
                question=input.question
            ).evaluate_answer()

        return evaluate

    def run(
            self, 
            input: Input,
            chunks_callback, 
            result_callback
        ):        
        """Versão síncrona para compatibilidade."""
        return asyncio.run(self.run_async(input, chunks_callback, result_callback))