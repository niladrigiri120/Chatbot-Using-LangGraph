import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_tavily import TavilySearch

from .model import chat_llm
from .rag import retriever_store, load_retriever, rewrite_query

load_dotenv()

# Tool 1
search_tool = TavilySearch()

# Tool 2
@tool
def stock_price_tool(symbol:str):
    "Fetch daily stock price"

    api_key = os.getenv("Alpha_Vantage_API")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()
    return data

# Tool 3
@tool
def rag_tool(query:str, config:RunnableConfig):
    """Use this tool to retrieve information from the uploaded PDF document.
    Always call this tool when answering questions about the document."""

    re_query = rewrite_query(query)
    thread_id = config["configurable"].get("thread_id")

    if thread_id in retriever_store:
        retriever = retriever_store[thread_id]           # Instead of loading from disk, it searches in Memory first
    else:
        retriever = load_retriever(thread_id)

    if retriever is None:
        return """
        No document is currently available.

        If the user uploads a document later, you must call rag_tool again to retrieve information from it.
        Documents may be uploaded or replaced during the conversation.
        """
    
    docs = retriever.invoke(re_query)
    if not docs:
        return "No relevant contents found"
    
    context = "\n".join(doc.page_content for doc in docs)

    return context

tools = [search_tool, stock_price_tool, rag_tool]

llm_with_tools = chat_llm.bind_tools(tools)