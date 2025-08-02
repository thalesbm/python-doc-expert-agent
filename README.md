#### Este projeto é um agente construído em Python com LangChain, que:

- [DONE] Utiliza RAG (Retrieval-Augmented Generation) para responder perguntas baseadas em documentos PDF.
- [DONE] Utiliza tools externas via function calling para complementar respostas com dados dinâmicos.
- [DONE] Utiliza uma interface para enviar as perguntas (Streamlit).
- [DONE] Utiliza Ragas para avaliar se o RAG realmente responde corretamente (Context Recall, Faithfulness, Answer Relevance).
- [DONE] Utiliza outros conceitos de prompt Engineering.
- [DONE] Utiliza ReAct para deixar o LLM decidir o que fazer até chegar na resposta final.
- [DONE] Utiliza ConversationSummaryMemory (memória com resumo).
- [DONE] Utiliza ConversationBufferMemory (histórico completo).
- [DONE] Utiliza tecnicas de Hiperparametrização par RAG

#### Parametros utilizados no RAG; 
- k (top_k): 5
- Chunk size: 1024
- Chunk overlap: 150
- Score Threshold: 0.8
- Retrieval Strategy: 20
- Temperatura: 0

## Configurações Disponíveis

### DatabaseConfig
- `chunk_size`: 512 bytes (otimizado para desenvolvimento)
- `chunk_overlap`: 100 bytes
- `top_k`: 3 documentos
- `fetch_k`: 10 documentos
- `score_threshold`: 0.8

### OpenAIConfig
- `model`: gpt-4o-mini
- `temperature`: 0.1 (pequena variação)
- `max_tokens`: 1000

### RagConfig
- `enable_evaluation`: true
- `evaluation_metrics`: ["answer_relevancy", "faithfulness"]

### LoggingConfig
- `level`: DEBUG
- `file_path`: logs/dev.log

### StreamlitConfig
- `page_title`: "Doc Expert Agent - DEV"
- `page_icon`: 🔧

#### Comandos:
```bash
pip3 install -r requirements.txt

python3 -m venv .venv

source .venv/bin/activate

python3 -m streamlit run doc-expert-agent/app.py

python3 ./doc-expert-agent/app.py
```

#### Validações
```bash
python3 ./doc-expert-agent/validation/validation_tcc.py
```
