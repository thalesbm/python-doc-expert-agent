#### Este projeto é um agente construído em Python com LangChain, que:

- [DONE] Utiliza RAG (Retrieval-Augmented Generation) para responder perguntas baseadas em documentos PDF.
- [DONE] Utiliza tools externas via function calling para complementar respostas com dados dinâmicos.
- [DONE] Utiliza uma interface para enviar as perguntas (Streamlit).
- [DONE] Utiliza Ragas para avaliar se o RAG realmente responde corretamente (Context Recall, Faithfulness, Answer Relevance).
- [DONE] Utiliza outros conceitos de prompt Engineering.
- [DONE] Utiliza ReAct para deixar o LLM decidir o que fazer até chegar na resposta final.
- [DONE] Utiliza ConversationSummaryMemory (memória com resumo).
- [DONE] Utiliza ConversationBufferMemory (histórico completo).
- [DOING] Utiliza tecnicas de Hiperparametrização par RAG

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
