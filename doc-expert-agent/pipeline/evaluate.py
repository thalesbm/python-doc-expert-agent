from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_recall
from datasets import Dataset

from model.answer import Answer

from typing import List

from logger import get_logger

logger = get_logger(__name__)

class Evaluate:

    def __init__(self, question: str, answer: str, chunks: List[Answer]):
        self.question = question
        self.answer = answer
        self.chunks = chunks

    def evaluate_answer(self):
        logger.info("Iniciando validação da resposta...")

        result = evaluate(
            self.set_dataset(),
            metrics=[answer_relevancy, faithfulness, context_recall]
        )

        logger.info(result)
        logger.info("Finalizado validação da resposta")

        return result

    def set_dataset(self):
        data = Dataset.from_dict({
            "question": [self.question],
            "answer": [self.answer],
            "reference": [self.answer], 
            "contexts": [[chunk.content for chunk in self.chunks]],
        })

        return data
