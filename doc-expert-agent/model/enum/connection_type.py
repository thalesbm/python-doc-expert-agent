from enum import Enum

class ConnectionType(Enum):
    BASIC_CONNECTION = "conexao-simples-llm"
    CONNECTION_WITH_COMPLETE_MEMORY = "conexao-llm-complete-memory"
    CONNECTION_WITH_SUMARY_MEMORY = "conexao-llm-summary-memory"
    CONNECTION_WITH_TOOLS = "conexao-com-tool"
    CONNECTION_WITH_TOOLS_AND_REACT = "conexao-com-tool-react"
