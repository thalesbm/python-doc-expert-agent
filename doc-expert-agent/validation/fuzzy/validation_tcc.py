from fuzzywuzzy import fuzz
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores.chroma import Chroma

import validation.questions

import os

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
    for item in validation.questions.avaliacao:
        pergunta = item["pergunta"]
        ideal = item["resposta_ideal"]
        resposta = obter_resposta_rag(vector_store, pergunta)
        score = fuzz.token_set_ratio(resposta, ideal)

        print(f"\nPergunta: {pergunta}")
        print(f"Esperado: {ideal}")
        print(f"Similaridade (0-100): {score}")

        if score >= 80:
            acertos += 1

    total = len(validation.questions.avaliacao)
    print(f"\nAcertos: {acertos}/{total} ({acertos/total*100:.1f}%)")

if __name__ == "__main__":
    vector_store = get_vector_store(
        api_key=os.getenv("OPENAI_API_KEY"),
        database_path="files/tcc/chroma_db/"
    )
    avaliar_rag(vector_store)
