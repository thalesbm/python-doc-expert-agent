from pipeline.loader import Loader
from pipeline.splitter import Splitter
from pipeline.embedding import Embedding
from pipeline.retrieval import Retrieval
from pipeline.openai import Key
from pipeline.evaluate import Evaluate

from service.select_service import SelectServices
from model.input import Input

import logging

logger = logging.getLogger(__name__)

class MainController:

    def __init__(self, connection_type: str):
        logger.info("Iniciando setup do RAG...")

        self.api_key = Key.get_openai_key()

        document = Loader.load_document(connection_type=connection_type)
        chunks = Splitter.split_document(document)
        self.vector_store = Embedding.embedding_document(chunks, self.api_key)

        logger.info("Setup do RAG finalizado!")

    def run(
            self, 
            input: Input,
            chunks_callback, 
            result_callback
        ):
        logger.info(f"Pergunta recebida: {input.question}")

        # retrieval
        chunks = Retrieval.retrieve_similar_documents(
            vector_store=self.vector_store, 
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
        evaluate = Evaluate(
            answer=result,
            chunks=chunks, 
            question=input.question
        ).evaluate_answer()

        return evaluate