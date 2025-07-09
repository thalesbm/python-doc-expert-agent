from langchain_openai.chat_models import ChatOpenAI

class OpenAIClientFactory:
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def create_basic_client(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0
        )

    def create_client_with_tools(self, tools) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0
        ).bind(functions=tools)