import openai
from colorama import Fore, Style, init

client = openai.Client(api_key = "")

init(autoreset=True)

def geracaoTexto(mensagens):
    resposta = client.chat.completions.create(
        messages= mensagens,
        model="gpt-3.5-turbo-0125",
        max_tokens=1000,
        temperature=0,
        stream=True
    )
    print(f"{Fore.RED}Bot:", end = "")
    
    text_completo = ""

    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end="")
            text_completo += texto
    print()
    mensagens.append({"role":"assistant", "content": text_completo})
    return mensagens

if __name__ == "__main__":
    print(f"{Fore.YELLOW}Bem vindo ao Chatbot")
    mensagens = []
    while True:
        in_user = input(f"{Fore.GREEN}User: {Style.RESET_ALL}")
        mensagens.append({"role": "user", "content": in_user})
        mensagens = geracaoTexto(mensagens)
