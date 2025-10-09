# 🧠 Agente Inteligente de Lista de Compras (MCP)

Este projeto implementa um **agente inteligente baseado em MCP (Model Context Protocol)**, capaz de gerenciar uma lista de compras usando comandos de voz e salvar os produtos em uma planilha Excel. O agente também permite enviar a lista via WhatsApp usando um link pré-preenchido.

## ✨Como funciona

O agente escuta comandos de voz, interpreta a linguagem natural com um modelo LLM, atualiza a planilha Excel e envia a lista via WhatsApp se solicitado.
Todas as alterações são salvas automaticamente, sem interface gráfica.

## ✨Funcionalidades do Agente

- Aceita **comandos de voz** para:
  - Adicionar produtos
  - Remover produtos
  - Listar produtos
  - Enviar lista via WhatsApp
- Mantém a lista de compras em **arquivo Excel (`.xlsx`)**
- Integração com **modelo LLM gratuito** (via Ollama/LangChain) para interpretar linguagem natural
- Não possui interface gráfica; todo funcionamento é via terminal

---

## ✨Bibliotecas utilizadas

- **openpyxl** — manipulação de planilhas Excel  
- **sounddevice** — entrada de voz  
- **vosk** — reconhecimento de voz offline  
- **langchain-ollama** — processamento de linguagem natural   
- **webbrowser** — envio da lista via WhatsApp  

> Obs.: Todas as bibliotecas são gratuitas e compatíveis com Python 3.10+.

---

## ✨ Como executar

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

2. Instale as dependências (estão todas em um único arquivo)
```bash
pip install -r requirements.txt
```
## ✨ Estrutura principal do projeto
```bash
├── agenteMCP.py # Script principal do agente
├── planilha.py # Gera a planilha lista_compras.xlsx
├── requirements.txt # Dependências do projeto
├── vosk-model-small/ # Modelo de reconhecimento de voz
└── README.md # Este arquivo
```

## ✨ Configuração do Ollama e Modelo Mistral

O **Ollama** permite rodar modelos de linguagem grandes (LLMs) localmente, sem depender de APIs externas.  
No projeto, usamos o modelo **Mistral** para interpretar comandos de voz.

### Passo a passo

#### 1. Instalação do Ollama

- Baixe o instalador do site oficial: [https://ollama.com](https://ollama.com)  
- Execute o instalador e abra o `Ollama.exe` pelo menos uma vez.

#### 2. Baixando o modelo Mistral

- Vá até a pasta do Ollama pelo terminal
 ```bash
cd "C:\Users\SeuUsuario\AppData\Local\Programs\Ollama\"
```
- Baixe o Mistral
```bash
ollama pull mistral
```

#### 3. Integração no Python

```python
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")

from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="mistral")


