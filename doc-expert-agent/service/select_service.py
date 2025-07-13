from typing import List
from model.answer import Answer
from model.enum.connection_type import ConnectionType
from model.enum.prompt_type import PromptType
from model.input import Input

from service.agent_basic.connection import BasicConnectionToOpenAI
from service.agent_basic_complete_memory.connection import BasicConnectionWithMemoryToOpenAI
from service.agent_tools.connection import ConnectionWithToolsToOpenAI
from service.agent_react.connection import ConnectionWithReactToOpenAI

import logging
logger = logging.getLogger(__name__)

class SelectServices:

    def __init__(self, answers: List[Answer], api_key: str):
        self.answers = answers
        self.api_key = api_key

    def run(
        self,
        input: Input
    ):

        logger.info("Inicializando SelectServices")

        if not self.answers:
            logger.warning("Nenhum contexto fornecido. Verifique se a lista de answers está vazia.")
            return

        result = ""

        type = ConnectionType(input.connection_type)

        if type == ConnectionType.BASIC_CONNECTION:
            result = self.basic_connect(input)

        elif type == ConnectionType.CONNECTION_WITH_TOOLS:
            result = self.connect_with_tools(input)

        elif type == ConnectionType.CONNECTION_WITH_TOOLS_AND_REACT:
            result = self.connect_with_tools_and_react(input)

        elif type == ConnectionType.BASIC_CONNECTION_WITH_COMPLETE_MEMORY:
            result = self.basic_connect_with_memory(input)

        logger.info("Finalizado SelectServices")    

        return result

    def basic_connect(self, input: Input):
        return BasicConnectionToOpenAI(
            context=self.get_context(), 
            question=input.question, 
            prompt_type=PromptType(input.prompt_type)
        ).connect(api_key=self.api_key)
    
    def basic_connect_with_memory(self, input: Input):
        return BasicConnectionWithMemoryToOpenAI(
            context=self.get_context(), 
            question=input.question
        ).connect(api_key=self.api_key)

    def connect_with_tools(self, input: Input):
        return ConnectionWithToolsToOpenAI(
            context=self.get_context(), 
            question=input.question, 
        ).connect(api_key=self.api_key)

    def connect_with_tools_and_react(self, input: Input):
        return ConnectionWithReactToOpenAI(
            context=self.get_context(), 
            question=input.question, 
        ).connect(api_key=self.api_key)

    def get_context(self) -> str:
        context = ""
        for ans in self.answers:
            context += ans.content + "\n---\n"

        return context
