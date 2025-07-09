#### Este projeto é um agente RAG construído em Python com LangChain, que:

- [DONE] Utiliza RAG para responder perguntas baseadas em documentos PDF
- [DONE] Utiliza tools externas via function calling para complementar respostas com dados dinâmicos
- [DONE] Utiliza uma interface para enviar as perguntas (Streamlit) 
- [DONE] Utiliza Ragas para avaliar se o RAG realmente responde corretamente (Context Recall, Faithfulness, Answer Relevance)
- [DONE] Utiliza outros conceitos de prompt Engineering
- [DONE] ReAct
- Adicione memoria

#### Comandos:
```bash
pip3 install -r requirements.txt

python3 -m venv .venv

source .venv/bin/activate

python3 -m streamlit run caso-de-uso/app.py

python3 ./caso-de-uso/app.py
```

#### Problemas:

- [DONE] A geração de respostas com base no context não está 100% correta