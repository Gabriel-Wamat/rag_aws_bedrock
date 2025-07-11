# 🧠 LangGraph RAG com AWS Bedrock + Streamlit

Aplicação simples RAG que responde perguntas com base sobre um Guia de LangGraph 

---

## 📚 Descrição 

- Lê e fragmenta um PDF técnico (guia do LangGraph)
- Usa **Titan Embeddings** para vetorização semântica
- Recupera os trechos mais relevantes por similaridade
- Usa o **Mistral 7B Instruct (via Bedrock)** para gerar respostas
- Interface interativa e amigável com Streamlit

---

## 🗂 Estrutura do projeto

📁 langgraph-rag/
app.py                 # Código principal (RAG + Interface)
langgraph_guide.pdf    # Documento base de conhecimento
.env                   # Variáveis de ambiente (chaves AWS)
requirements.txt       # Dependências do projeto
.gitignore             # Itens ignorados pelo Git

---

## 🔧 Requisitos

- Python 3.10 ou superior
- Conta AWS com permissões de uso para:
  - `mistral.mistral-7b-instruct-v0:2`
  - `amazon.titan-embed-text-v2:0`

---

## 📦 Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/langgraph-rag.git
cd langgraph-rag
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
## 🔐 Configuração do .env

AWS_ACCESS_KEY_ID=SEU_ID
AWS_SECRET_ACCESS_KEY=SEU_SEGREDO
AWS_DEFAULT_REGION=us-east-1

## Execução do app
streamlit run app.py

## 🛠 Tecnologias usadas
	•	LangGraph
	•	LangChain
	•	Amazon Bedrock
	•	Titan Embeddings
	•	Mistral 7B Instruct
	•	Streamlit
