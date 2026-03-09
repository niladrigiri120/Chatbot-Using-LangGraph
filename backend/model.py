import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

chat_llm = ChatGroq(model= "openai/gpt-oss-120b", api_key= os.getenv("GROQ_API_KEY"))
title_llm = ChatGroq(model= "openai/gpt-oss-20b", api_key= os.getenv("GROQ_API_KEY"))

@st.cache_resource
def load_embed():
    return HuggingFaceEmbeddings(model= "sentence-transformers/all-MiniLM-L12-v2") 
