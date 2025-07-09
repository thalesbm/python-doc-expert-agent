from typing import List
from model.answer import Answer
from model.enum.connection_type import ConnectionType
from model.enum.prompt_type import PromptType

from service.agent_basic.connection import BaseConnectionToOpenAI
from service.agent_tools.connection import ConnectionWithToolsToOpenAI
from service.agent_react.connection import ConnectionWithReactToOpenAI

import logging
logger = logging.getLogger(__name__)

class SelectServices:

    def __init__(self, answers: List[Answer], question: str, api_key: str):
        self.answers = answers
        self.question = question
        self.api_key = api_key

    def run(
        self,
        connection_type: str,
        prompt_type: str
    ):

        logger.info("Inicializando SelectServices")

        if not self.answers:
            logger.warning("Nenhum contexto fornecido. Verifique se a lista de answers está vazia.")
            return

        result = ""

        type = ConnectionType(connection_type)

        if type == ConnectionType.BASIC_CONNECTION:
            result = self.base_connect(prompt_type)

        elif type == ConnectionType.CONNECTION_WITH_TOOLS:
            result = self.connect_with_tools()

        elif type == ConnectionType.CONNECTION_WITH_TOOLS_AND_REACT:
            result = self.connect_with_tools_and_react()

        logger.info("Finalizado SelectServices")    

        return result

    def base_connect(self, prompt_type: str):
        return BaseConnectionToOpenAI(
            context=self.get_context(), 
            question=self.question, 
            prompt_type=PromptType(prompt_type)
        ).connect(api_key=self.api_key)

    def connect_with_tools(self):
        return ConnectionWithToolsToOpenAI(
            context=self.get_context(), 
            question=self.question, 
        ).connect(api_key=self.api_key)

    def connect_with_tools_and_react(self):
        return ConnectionWithReactToOpenAI(
            context=self.get_context(), 
            question=self.question, 
        ).connect(api_key=self.api_key)

    def get_context(self) -> str:
        context = ""
        for ans in self.answers:
            context += ans.content + "\n---\n"

        return context
