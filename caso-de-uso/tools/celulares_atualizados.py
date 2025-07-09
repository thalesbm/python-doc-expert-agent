from langchain_core.utils.function_calling import convert_to_openai_function

from langchain.agents import tool
import time

def get_tools():
    return [convert_to_openai_function(celulares_atualizados)]

def get_simple_tools():
    return [celulares_atualizados]

@tool
def celulares_atualizados() -> str:
    """
    Retorne a quantidade de celulares disponíveis no mercado em 2025. 
    SEMPRE chame esta função para perguntas sobre quantidade de celulares, compatibilidade ou modelos disponíveis.
    """
    time.sleep(3)
    return "20.000"