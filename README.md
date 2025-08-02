# Doc Expert Agent

Um agente inteligente construído em Python que utiliza **RAG (Retrieval-Augmented Generation)** para responder perguntas baseadas em documentos PDF.

## Funcionalidades

- **RAG (Retrieval-Augmented Generation)**: `Sistema completo de busca e geração baseada em documentos`
- **Chunking Adaptativo**: `Divisão inteligente de documentos baseada no conteúdo`
- **Tools**: `Integração com ferramentas externas via function calling`
- **Interface**: `Interface web com Streamlit`
- **Avaliação**:` Métricas de qualidade com Ragas`
- **Memória**: `Suporte a memória completa e resumida`
- **ReAct**: `Raciocínio e ação para decisões inteligentes`
- **Prompt Engineering**: `Técnicas avançadas de engenharia de prompts`
- **Hiperparâmetros**: `Configuração otimizada para RAG`
- **LangSmith**: `Integração com LangSmith para avaliar respostas`

## Como Usar

#### Configuração do arquivo .env
Crie o arquivo .env na raiz do projeto e copie código abaixo:

```bash
# Chave da OpenAI
OPENAI_API_KEY=ADICIONE A CHAVE DA OPEN AI

# Configurações de logging
LOG_LEVEL=DEBUG
LOG_FILE=dev.log
LOG_CONSOLE=true
LOG_FILE_OUTPUT=true 

# Configuração do LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="ADICIONA A CHAVE DO LANGSMITH"
LANGSMITH_PROJECT="doc-expert-agent"
```

### Execução
```bash
# Ative o ambiente virtual (opcional)
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

# Execute a aplicação
python3 -m streamlit run doc-expert-agent/app.py
```

### Validação
```bash
# Execute os testes de validação
python3 ./doc-expert-agent/validation/validation_tcc.py
```

## Configurações

### OpenAI
- **Modelo**: `gpt-4o-mini`
- **Temperatura**: `0`
- **Tokens máximos**: `1000`

### RAG
- **Tamanho do chunk**: `1024 bytes`
- **Overlap**: `150 bytes`
- **Top K**: `5`
- **Fetch K**: `20`
- **Score threshold**: `0.85`
- **Avaliação**: `Habilitada`

## Métricas de Avaliação

- **Context Recall**: `Relevância do contexto encontrado`
- **Faithfulness**: `Fidelidade da resposta ao contexto`
- **Answer Relevance**: `Relevância da resposta para a pergunta`
