from abc import ABC, abstractmethod
from typing import List
from langchain.schema import BaseMessage
from model.input import Input
from model.answer import Answer

class ConnectInterface(ABC):
    """Interface abstrata para conexão com a API do OpenAI."""

    @abstractmethod
    def connect(self, api_key: str) -> str:
        pass
