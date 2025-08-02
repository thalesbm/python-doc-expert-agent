from typing import Any, Dict
from infra.openai_client import OpenAIClientFactory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks.base import BaseCallbackHandler
from tools.celulares_atualizados import get_simple_tools
from service.agent_react.prompt import Prompt

from logger import get_logger

logger = get_logger(__name__)

class ConnectionWithReactToOpenAI:
    """Classe responsável por conectar com OpenAI usando ReAct (Reasoning and Acting)."""

    def __init__(self, context: str, question: str) -> None:
        self.context: str = context
        self.question: str = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI...")

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        prompt = Prompt.get_react_prompt()
        tools = get_simple_tools()
        agent = create_openai_tools_agent(chat, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True, callbacks=[LogHandler()])

        result: Dict[str, Any] = executor.invoke({"query": self.question, "context": self.context})
        output: str = result.get("output", "")
        
        logger.info("===================================")
        logger.info(f"OpenAI: {output}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI")

        return output
    
class LogHandler(BaseCallbackHandler):
    """Handler para logging das ações do agente ReAct."""
    
    def on_agent_action(self, action: Dict[str, Any], **kwargs: Any) -> None:
        """Log quando o agente executa uma ação."""
        logger.info(f"Agente executou: {action.get('tool', 'Unknown tool')}")
        logger.info(f"Input: {action.get('tool_input', 'No input')}")
    
    def on_agent_finish(self, finish: Dict[str, Any], **kwargs: Any) -> None:
        """Log quando o agente finaliza."""
        logger.info(f"Agente finalizou: {finish.get('output', 'No output')}")
