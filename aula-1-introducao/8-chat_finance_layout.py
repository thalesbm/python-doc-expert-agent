import yfinance as yf
import openai
import json
# import pandas as pd
import streamlit as st

client = openai.Client(api_key = "")

def retorna_cotacao(ticker, periodo="1mo"):
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period = periodo)["Close"]
    # hist.index = hist.index.strftime("%Y-%m-%d")
    # hist.index = pd.to_datetime(hist.index).strftime("%Y-%m-%d")
    hist.index = hist.index.map(lambda x: x.strftime("%Y-%m-%d"))
    hist = round(hist, 2)
    
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[::-slice_size][::-1]

    return hist.to_json()

tools = [
    {
        "type": "function",
        "function": {
            "name": "retorna_cotacao",
            "description": "Retorna a cotacao das acoes da ibovespa",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string", 
                        "description": "O ticker da acao"
                    },
                    "periodo": {
                        "type": "string", 
                        "description": "O periodo da consulta",
                        "enum": ["1d", "5d", "1mo", "6mo", "1y", "5y", "10y", "ytd", "max"]
                    }
                }
            }
        }
    }
]

funcao_disponivel = {"retorna_cotacao": retorna_cotacao}

def gera_texto(mensagens):
    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=mensagens,
        tools=tools,
        tool_choice="auto",
    )

    tools_calls = resposta.choices[0].message.tool_calls
    # print(tools_calls)

    if tools_calls:
        mensagens.append(resposta.choices[0].message)
        for tool_call in tools_calls:
            function_name = tool_call.function.name
            function_to_call = funcao_disponivel[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_return = function_to_call(**function_args)

            mensagens.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_return,
                }
            )
        
            segunda_resposta = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=mensagens,
            )

            mensagens.append(segunda_resposta.choices[0].message)
    
    return mensagens

st.set_page_config(page_title="ChatBot Financeiro")
st.title("ChatBot de cotacao de acoes")

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

for msg in st.session_state.mensagens:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

user_input = st.chat_input("Digite")
if user_input:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state.mensagens.append({"role": "user", "content": user_input})
    st.chat_message("user").markdown(user_input)
    
    # Processa a mensagem
    st.session_state.mensagens = gera_texto(st.session_state.mensagens)

    # Exibe a resposta do chatbot
    ultima_mensagem = st.session_state.mensagens[-1]
    if ultima_mensagem.role == "assistant":
        st.chat_message("assistant").markdown(ultima_mensagem.content)