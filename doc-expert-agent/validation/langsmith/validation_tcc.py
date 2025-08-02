from langsmith.evaluation import RunEvaluator, evaluate
from langsmith.schemas import Example

from model.input import Input
from service.agent_basic.connection import BasicConnectionToOpenAI
from model.enum.prompt_type import PromptType

import validation.questions
import os

def minha_chain(inputs):
    question = inputs["question"]
    
    resposta = basic_connect(question)
    
    return resposta

def basic_connect(question: str):
    api_key = os.getenv("OPENAI_API_KEY")

    return BasicConnectionToOpenAI(
        context=get_context(), 
        question=question, 
        prompt_type=PromptType.FEW_SHOT_PROMPT
    ).connect(api_key=api_key)

def run_evaluators():
    examples = [
        Example(
            inputs={"question": item["pergunta"]},
            outputs={"resposta_ideal": item["resposta_ideal"]}
        )
        for item in validation.questions.avaliacao
    ]

    evaluator = RunEvaluator.auto()

    results = evaluate(
        chain=minha_chain,
        data=examples,
        evaluators=[evaluator],
        experiment_prefix="RAG_TCC"
    )

    for r in results:
        print(f"Input: {r.input}")
        print(f"Esperado: {r.outputs['resposta_ideal']}")
        print(f"Gerado: {r.result}")
        print(f"Score: {r.score}")

if __name__ == "__main__":
    run_evaluators()
