from pipeline.loader import Loader
from pipeline.splitter import Splitter
from pipeline.embedding import Embedding
from pipeline.retrieval import Retrieval
from pipeline.openai import Key
from pipeline.evaluate import Evaluate

from service.select_service import SelectServices
from model.input import Input
from config import get_config
from infra import get_logger

logger = get_logger(__name__)

class MainController:

    def __init__(self, connection_type: str, database_path: str):
        logger.info("Iniciando setup do RAG...")

        self.database_path = database_path
        self.config = get_config()

        self.api_key = Key.get_openai_key()

        document = Loader.load_document(connection_type=connection_type)
        chunks = Splitter.split_document(document)
        
        Embedding.embedding_document(chunks, self.api_key, database_path)

        logger.info("Setup do RAG finalizado!")

    def run(
            self, 
            input: Input,
            chunks_callback, 
            result_callback
        ):        
        logger.info(f"Pergunta recebida: {input.question}")

        # retrieval
        chunks = Retrieval().retrieve_similar_documents(
            database_path=self.database_path.value,
            api_key=self.api_key,
            question=input.question
        )
        chunks_callback(chunks)

        # open ai
        result = SelectServices(
            answers=chunks,
            api_key=self.api_key,
        ).run(
            input=input
        )
        result_callback(result)

        # evaluate
        evaluate = None
        if self.config.rag.enable_evaluation:
            evaluate = Evaluate(
                answer=result,
                chunks=chunks, 
                question=input.question
            ).evaluate_answer()

        return evaluate