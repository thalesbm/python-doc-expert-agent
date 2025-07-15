from fuzzywuzzy import fuzz
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores.chroma import Chroma

import os

avaliacao = [
    {
        "pergunta": "quem escreveu o projeto?",
        "resposta_ideal": "Marlon Iwanaga Pacheco, Rafael Cinquini, Raphael Farias Utida, Thales Bertolini Marega"
    },
    {
        "pergunta": "qual o titulo do trabalho?",
        "resposta_ideal": "O título do trabalho é SISTEMAS MÓVEIS NO MUNDO ACADÊMICO E SUA IMPORTÂNCIA AO DESENVOLVIMENTO COMPUTACIONAL"
    },
    {
        "pergunta": "em que ano foi escrito?",
        "resposta_ideal": "O TCC foi escrito em 2014."
    },
    {
        "pergunta": "qual o nome do aplicativo desenvolvido?",
        "resposta_ideal": "Calculadora de Fisica"
    },
    {
        "pergunta": "qual linguagem o aplicativo foi escrito?",
        "resposta_ideal": "O aplicativo foi escrito utilizando principalmente as linguagens JavaScript e HTML."
    },
    {
        "pergunta": "qual o objetivo do projeto?",
        "resposta_ideal": "O objetivo é facilitar a adaptação e integração entre as principais plataformas móveis, Android e iOS, e analisar o impacto dessa aplicação no contexto educacional, proporcionando um método alternativo de aprendizado interativo e envolvente."
    },
]

def get_vector_store(api_key: str, database_path: str):
    vector_store = Chroma(
        embedding_function=OpenAIEmbeddings(api_key=api_key),
        persist_directory=database_path
    )
    return vector_store

def obter_resposta_rag(vector_store, pergunta):
    docs = vector_store.max_marginal_relevance_search(
        query=pergunta,
        k=5,
        fetch_k=20,
        score_threshold=0.85,
    )

    resposta = " ".join([doc.page_content for doc in docs])
    return resposta.strip()

def avaliar_rag(vector_store):
    acertos = 0
    for item in avaliacao:
        pergunta = item["pergunta"]
        ideal = item["resposta_ideal"]
        resposta = obter_resposta_rag(vector_store, pergunta)
        score = fuzz.token_set_ratio(resposta, ideal)

        print(f"\nPergunta: {pergunta}")
        print(f"Esperado: {ideal}")
        print(f"Similaridade (0-100): {score}")

        if score >= 80:
            acertos += 1

    total = len(avaliacao)
    print(f"\nAcertos: {acertos}/{total} ({acertos/total*100:.1f}%)")

if __name__ == "__main__":
    vector_store = get_vector_store(
        api_key=os.getenv("OPENAI_API_KEY"),
        database_path="files/tcc/chroma_db/"
    )
    avaliar_rag(vector_store)
