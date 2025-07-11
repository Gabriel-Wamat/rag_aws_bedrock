# app.py

import os
import streamlit as st
import boto3
from dotenv import load_dotenv
from typing_extensions import TypedDict, List

from langchain_aws import ChatBedrockConverse, BedrockEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, StateGraph

#  1. Config .env 
load_dotenv()

# 2. AWS e Bedrock 
bedrock_client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION"))

llm = ChatBedrockConverse(
    client=bedrock_client,
    model='mistral.mistral-7b-instruct-v0:2'  
)

embeddings = BedrockEmbeddings(
    client=bedrock_client,
    model_id="amazon.titan-embed-text-v2:0"
)

# 3. Carregar e vetorar PDF 
vector_store = InMemoryVectorStore(embeddings)

loader = PyPDFLoader("langgraph_guide.pdf")  
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = splitter.split_documents(docs)

vector_store.add_documents(splits)

# 4. Pipeline 
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    docs = vector_store.similarity_search(state["question"])
    return {"context": docs}

prompt = ChatPromptTemplate.from_template(
    "Você é um assistente técnico especializado em LangGraph. Responda com base apenas no guia abaixo.Toda a resposta tem que ser em português brasileiro\n"
    "Se a resposta não estiver claramente contida, diga que não sabe.\n\n"
    "Contexto:\n{context}\n\nPergunta: {question}"
)

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({
        "question": state["question"],
        "context": docs_content
    })
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

def responder_pergunta(pergunta: str) -> str:
    result = graph.invoke({"question": pergunta})
    return result["answer"]

# 5. Interface  
st.set_page_config(page_title="LangGraph RAG", layout="centered")

st.title("RAG - Pergunte sobre o LangGraph")
st.caption("Baseado no conteúdo do PDF 'langgraph_guide.pdf'")

pergunta = st.text_input("Digite sua pergunta:")
if st.button("Enviar") and pergunta:
    with st.spinner("Buscando resposta..."):
        try:
            resposta = responder_pergunta(pergunta)
            st.markdown("## 📣 Resposta:")
            st.success(resposta)
        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")