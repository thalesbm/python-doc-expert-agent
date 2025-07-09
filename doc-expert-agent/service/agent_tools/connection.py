from infra.openai_client import OpenAIClientFactory
from tools.celulares_atualizados import get_tools
from tools.celulares_atualizados import celulares_atualizados
from service.agent_tools.prompt import Prompt

import logging

logger = logging.getLogger(__name__)

class ConnectionWithToolsToOpenAI:

    def __init__(self, context: str, question: str):
        self.context = context
        self.question = question

    def connect(self, api_key: str) -> str:
        logger.info("Iniciando conexão com a open AI...")

        chat = OpenAIClientFactory(api_key=api_key).create_client_with_tools(get_tools())

        prompt = Prompt.get_entry_prompt()
        chain = prompt | chat

        result = chain.invoke({'query': self.question, "context": self.context})

        value = self.configure_function_call(result)

        follow_up_chain = Prompt.get_exit_prompt() | chat

        follow_up_result = follow_up_chain.invoke({
            "resposta": result.content,
            "valor": value
        })

        logger.info("===================================")
        logger.info(f"OpenAI: {follow_up_result.content}")
        logger.info("===================================")

        logger.info("Finalizando conexão com a open AI")

        return follow_up_result.content

    def configure_function_call(self, result) -> str:
        if result.additional_kwargs.get("function_call"):
            func_name = result.additional_kwargs["function_call"]["name"]
            logger.info(f"Function Call: {func_name}")

            if func_name in ["celulares_atualizados()", "celulares_atualizados"]:
                valor = celulares_atualizados.invoke({})
                logger.info(f"Function Result: {valor}")
                return valor

        logger.warning("LLM não executou a tool")
        logger.warning(result.content)
        return ""
