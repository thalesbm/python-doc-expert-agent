from service.agent_basic_complete_memory.prompt import Prompt

from langchain.memory import ConversationBufferMemory
from infra.openai_client import OpenAIClientFactory

import logging

logger = logging.getLogger(__name__)

memory = ConversationBufferMemory()

class BasicConnectionWithMemoryToOpenAI:

    def __init__(self, context: str, question: str):
        self.context = context
        self.question = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI do documento...")

        prompt = Prompt(context=self.context, question=self.question, memory=memory.buffer).default_prompt()

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        logger.info(prompt)

        response = chat.invoke(prompt)

        logger.info("===================================")
        logger.info(f"User: {self.question}")
        logger.info("===================================")
        logger.info(f"OpenAI: {response.content}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI do documento")

        memory.save_context({"input": self.question}, {"output": response.content})

        return response.content
