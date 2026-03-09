import streamlit as st
from typing import Annotated
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from .tools import tools, llm_with_tools
from .database import checkpointer

# Create state
class ChatState(BaseModel):
    messages : Annotated[list[BaseMessage], add_messages]

# System prompt
system_prompt = SystemMessage(
    content="""
        You are Chatterly, an AI assistant created by Niladri Giri.

        Use tools whenever they can provide more accurate information.

        Tool rules:
        - If the user asks about an uploaded document, call rag_tool to retrieve the relevant content before answering.
        - Documents may be uploaded or replaced at any time in the conversation.
        - Always retrieve fresh information instead of relying on earlier responses.
        - Use the search tool for current events or information not related to the uploaded document.
        - Use stock_price_tool when the user asks for stock prices.

        Important:
        - Do not repeatedly call the same tool for the same question.
        - If a tool does not provide the needed information, answer using the available information instead of calling the tool again.
        - Do not guess document content without using rag_tool.
        """
        )
# Node 1
def chatbot_node(state:ChatState):
    message = [system_prompt ]+ state.messages
    response = llm_with_tools.invoke(message)

    return {
        "messages" : [response]
    }

# Node 2
tool_node = ToolNode(tools)         # It is also a node but dont need to write function for it

# Building graph
@st.cache_resource
def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("Chat Node", chatbot_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "Chat Node")
    graph.add_conditional_edges("Chat Node", tools_condition)
    graph.add_edge("tools", "Chat Node")
    graph.add_edge("Chat Node", END)

    chatbot = graph.compile(checkpointer=checkpointer)
    return chatbot
