from infra.openai_client import OpenAIClientFactory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks.base import BaseCallbackHandler
from tools.celulares_atualizados import get_simple_tools
from service.agent_react.prompt import Prompt

import logging

logger = logging.getLogger(__name__)

class ConnectionWithReactToOpenAI:

    def __init__(self, context: str, question: str):
        self.context = context
        self.question = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI...")

        chat = OpenAIClientFactory(api_key=api_key).create_basic_client()

        prompt = Prompt.get_react_prompt()
        tools = get_simple_tools()
        agent = create_openai_tools_agent(chat, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True, callbacks=[LogHandler()])

        result = executor.invoke({"query": self.question, "context": self.context})
        output = result.get("output")
        
        logger.info("===================================")
        logger.info(f"OpenAI: {output}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI")

        return output
    
class LogHandler(BaseCallbackHandler):
    def on_agent_action(self, action, **kwargs):
        logger.info(f"[LOG] Action: {action.tool} | Input: {action.tool_input}")

    def on_tool_end(self, output, **kwargs):
        logger.info(f"[LOG] Tool Output: {output}")

    def on_chain_end(self, outputs, **kwargs):
        logger.info(f"[LOG] Final Answer: {outputs}")
