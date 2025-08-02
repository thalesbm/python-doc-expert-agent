from langchain_openai.chat_models import ChatOpenAI
from config import get_config

class OpenAIClientFactory:
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        config = get_config()
        self.model = model or config.openai.model

    def create_basic_client(self) -> ChatOpenAI:
        config = get_config()
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=config.openai.temperature,
            max_tokens=config.openai.max_tokens
        )

    def create_client_with_tools(self, tools) -> ChatOpenAI:
        config = get_config()
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=config.openai.temperature,
            max_tokens=config.openai.max_tokens
        ).bind(functions=tools)