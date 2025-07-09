from service.agent_basic_memory.prompt import Prompt
from infra.openai_client import OpenAIClientFactory

import logging

logger = logging.getLogger(__name__)

class BasicConnectionWithMemoryToOpenAI:

    def __init__(self, context: str, question: str):
        self.context = context
        self.question = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI do documento...")

        prompt = Prompt(context=self.context, question=self.question).default_prompt()

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        response = chat.invoke(prompt)

        logger.info("===================================")
        logger.info(f"OpenAI: {response.content}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI do documento")

        return response.content
