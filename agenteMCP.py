from openpyxl import load_workbook #para arquivos excel
import webbrowser #para abrir o navegador
from urllib.parse import quote #para formatar a URL
import sounddevice #para reconhecimento de voz
import vosk #para reconhecimento de voz
import queue #para reconhecimento de voz
import json #para reconhecimento de voz
import os  #para manipulação de arquivos
from langchain_community.llms import Ollama #para LLM

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄

ARQUIVO = "lista_compras.xlsx"


#manipulação da lista de compras
def adicionar_produto(produto):
    wb = load_workbook(ARQUIVO)
    ws = wb.active
    ws.append([produto])
    wb.save(ARQUIVO)
    print(f"Produto '{produto}' adicionado a lista com sucesso!")

def remover_produto(produto):
    wb = load_workbook(ARQUIVO)
    ws = wb.active
    encontrado = False
    for row in ws.iter_rows(min_row=2): # pula o cabeçalho
        if row[0].value.lower() == produto.lower():
            ws.delete_rows(row[0].row)
            encontrado = True
            break
    wb.save(ARQUIVO)
    if encontrado:
        print(f"Produto '{produto}' removido da lista!")
    else:
        print(f"Produto '{produto}' não encontrado na lista.")

def listar_produtos():
    wb = load_workbook(ARQUIVO)
    ws = wb.active
    produtos = [row[0].value for row in ws.iter_rows(min_row=2)]
    if produtos:
        print("Lista de compras: ")
        for p in produtos:
            print("-", p)
    else:
        print("A lista de compras está vazia.")

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄

#para enviar a lista pelo whatsapp

def enviar_wpp():
    wb = load_workbook(ARQUIVO)
    ws = wb.active
    produtos = [row[0].value for row in ws.iter_rows(min_row=2)]
    if not produtos:
        print("A lista de compras está vazia. Nada há para enviar.")
        return
    mensagem = "Minha lista de compras:\n" + "\n".join(produtos)
    url = f"https://wa.me/?text={quote(mensagem)}"
    webbrowser.open(url)
    print("Abrindo WhatsApp para enviar a lista...")

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂

# Reconhecimento de voz
def ouvir_comando():
    q = queue.Queue()
    model = vosk.Model("vosk-model-small-pt-0.3")

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawImputStream(samplerate=16000, blocksize = 8000, dtype='int16',
                                channels=1, callback=callback):
        print("Diga um comando (como adicionar, remover, listar, enviar ou sair):")
        while True:
            data = q.get()
            if model.accept_waveform(data):
                result = json.loads(model.result())
                return result['text'].lower()
    
#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂

# Interpretar comandos com LLM

llm = Ollama(model="ollama3")

def interpretar_comando(texto):
    prompt = f"""
    Você é um assistente que interpreta comando de voz para um agente de lista de compras.
    Retorne apenas a ação e o produto (se aplicável) no formato: ação|produto
    Comandos possíveis: adicionar, remover, listar, enviar
    Exemplo: "Adicionar maçã" -> "adicionar|maçã"
    Exemplo: "Remover banana" -> "remover|banana"
    Comando: {texto}
    """
    resposta = llm(prompt)
    return resposta.strip()

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂

# Executar os comandos 

def executar_comando(resposta):
    if "|" in resposta:
        acao, produto = resposta.split("|", 1)
    else:
        acao, produto = resposta, ""
    
    if acao.lower() == "adicionar" and produto:
        adicionar_produto(produto)
    elif acao.lower() == "remover" and produto:
        remover_produto(produto)
    elif acao.lower() == "listar":
        listar_produtos()
    elif acao.lower() == "enviar":
        enviar_wpp()
    else:
        print("Comando inválido, tente novamente.")

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂

# Loop principal
while True:
    comando = ouvir_comando()
    if comando.lower() in ["sair", "encerra", "fim", "fechar"]:
        print("O agente está encerrando. Até mais!")
        break
    if comando:
        resposta = interpretar_comando(comando)
        executar_comando(resposta)

