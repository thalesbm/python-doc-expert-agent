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
