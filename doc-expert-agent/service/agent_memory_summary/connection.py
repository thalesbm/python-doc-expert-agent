from typing import List, Optional
from service.agent_memory_complete.prompt import Prompt

from langchain.memory import ConversationSummaryMemory
from infra.openai_client import OpenAIClientFactory
from langchain.schema import BaseMessage

from logger import get_logger

logger = get_logger(__name__)

class ConnectionWithSummaryMemoryToOpenAI:
    """Classe responsável por conectar com OpenAI usando memória resumida de conversa."""

    memory: Optional[ConversationSummaryMemory] = None

    def __init__(self, context: str, question: str) -> None:
        self.context: str = context
        self.question: str = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI do documento...")

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        if ConnectionWithSummaryMemoryToOpenAI.memory is None:
            ConnectionWithSummaryMemoryToOpenAI.memory = ConversationSummaryMemory(llm=chat)

        memory: ConversationSummaryMemory = ConnectionWithSummaryMemoryToOpenAI.memory

        prompt: List[BaseMessage] = Prompt(context=self.context, question=self.question, memory=memory.buffer).default_prompt()

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
