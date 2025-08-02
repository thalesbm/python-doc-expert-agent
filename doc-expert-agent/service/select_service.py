from typing import List, Optional
from model.answer import Answer
from model.enum.connection_type import ConnectionType
from model.enum.prompt_type import PromptType
from model.input import Input

from service.agent_basic.connection import BasicConnectionToOpenAI
from service.agent_memory_complete.connection import ConnectionWithCompleteMemoryToOpenAI
from service.agent_memory_summary.connection import ConnectionWithSummaryMemoryToOpenAI
from service.agent_tools.connection import ConnectionWithToolsToOpenAI
from service.agent_react.connection import ConnectionWithReactToOpenAI

from logger import get_logger

logger = get_logger(__name__)

class SelectServices:
    """Classe responsável por selecionar e executar o serviço apropriado baseado no tipo de conexão."""

    def __init__(self, answers: List[Answer], api_key: str) -> None:
        self.answers: List[Answer] = answers
        self.api_key: str = api_key

    def run(self, input: Input) -> Optional[str]:
        logger.info("Inicializando SelectServices")

        if not self.answers:
            logger.warning("Nenhum contexto fornecido. Verifique se a lista de answers está vazia.")
            return None

        result: str = ""

        connection_type: ConnectionType = ConnectionType(input.connection_type)

        if connection_type == ConnectionType.BASIC_CONNECTION:
            result = self.basic_connect(input)

        elif connection_type == ConnectionType.CONNECTION_WITH_TOOLS:
            result = self.connect_with_tools(input)

        elif connection_type == ConnectionType.CONNECTION_WITH_TOOLS_AND_REACT:
            result = self.connect_with_tools_and_react(input)

        elif connection_type == ConnectionType.CONNECTION_WITH_COMPLETE_MEMORY:
            result = self.basic_connect_with_complete_memory(input)

        elif connection_type == ConnectionType.CONNECTION_WITH_SUMARY_MEMORY:
            result = self.basic_connect_with_summary_memory(input)

        logger.info("Finalizado SelectServices")    

        return result

    def basic_connect(self, input: Input) -> str:
        context: str = self._build_context()
        prompt_type: PromptType = PromptType(input.prompt_type)
        
        connection = BasicConnectionToOpenAI(
            context=context,
            question=input.question,
            prompt_type=prompt_type
        )
        
        return connection.connect(self.api_key)

    def connect_with_tools(self, input: Input) -> str:
        context: str = self._build_context()
        
        connection = ConnectionWithToolsToOpenAI(
            context=context,
            question=input.question
        )
        
        return connection.connect(self.api_key)

    def connect_with_tools_and_react(self, input: Input) -> str:
        context: str = self._build_context()
        
        connection = ConnectionWithReactToOpenAI(
            context=context,
            question=input.question
        )
        
        return connection.connect(self.api_key)

    def basic_connect_with_complete_memory(self, input: Input) -> str:
        context: str = self._build_context()
        
        connection = ConnectionWithCompleteMemoryToOpenAI(
            context=context,
            question=input.question
        )
        
        return connection.connect(self.api_key)

    def basic_connect_with_summary_memory(self, input: Input) -> str:
        context: str = self._build_context()
        
        connection = ConnectionWithSummaryMemoryToOpenAI(
            context=context,
            question=input.question
        )
        
        return connection.connect(self.api_key)

    def _build_context(self) -> str:
        """Constrói o contexto a partir das respostas."""
        context_parts: List[str] = []
        
        for answer in self.answers:
            context_parts.append(answer.content)
        
        return "\n\n".join(context_parts)
