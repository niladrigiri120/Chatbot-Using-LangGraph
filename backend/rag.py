import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st

from .model import chat_llm, load_embed

retriever_store = {}

# Build retriever when file uploaded
def get_retriever(file_path: str, thread_id: str, embed_model):   

    loader = PyPDFLoader(file_path)                                                 # Load the document
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size= 800, chunk_overlap= 150)  # Chunk the documents
    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, embed_model)                                  # Embed and store into vectorDB

    path = f"vectorstores/{thread_id}"                                              # Save index
    db.save_local(path)

    retriever = db.as_retriever(search_type= "mmr", search_kwargs= {"k":5})  # Create retriever

    retriever_store[thread_id] = retriever                                          # Store inside a dictionary (thread_id : retriever)
    return retriever

# Load from vectorstore(disk), needed for server restart recovery.
def load_retriever(thread_id: str):

    path = f"vectorstores/{thread_id}"

    if not os.path.exists(path):
        return None
    
    embed_model = load_embed()
    db = FAISS.load_local(
        path,
        embed_model,
        allow_dangerous_deserialization=True
    )
    retriever = db.as_retriever(search_type= "mmr", search_kwargs= {"k":5})
    return retriever

# Query rewritten for better retrieval
def rewrite_query(query):

    prompt = f"""
        Rewrite the user query to improve document retrieval.

        Return ONLY the improved search query.
        Do NOT include explanations.

        Query: {query}
        """
    result = chat_llm.invoke(prompt)
    return result.content.strip()

# from sentence_transformers import CrossEncoder

# Reranker
# @st.cache_resource
# def rerank(query, docs):
#     reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
#     pairs = [[query, doc.page_content] for doc in docs]
#     scores = reranker.predict(pairs)

#     ranked = sorted(
#         zip(scores, docs),
#         key=lambda x: x[0],
#         reverse=True
#     )

#     return [doc for _, doc in ranked[:2]]