import os
import streamlit as st
from uuid import uuid4
from random import choice
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage

from backend.model import title_llm, load_embed
from backend.rag import get_retriever

state = st.session_state

# Function 1
def show_welcome():
    welcome_msg = ["Where should we start?",
                "What’s on your mind?",
                "Ready when you are.",
                "What should we work on?",
                "What would you like to explore?"]

    hour = datetime.now().hour

    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"

    if not state.message_history:
        st.markdown(f"""
            <div style="text-align:left; margin-top:100px; opacity:0.85;">
                <h3 style="margin-bottom:0px; font-weight:normal; line-height:1;">✴ Hey, {greeting}</h3>
                <h1 style="margin-top:0; font-weight:normal; line-height:1;">{choice(welcome_msg)}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

# Function 2
def conversation_loader(chatbot):

    for table in state.id_history:
        thread_id = table["id"]
        title = table["title"]

        if st.button(title, key=thread_id):
            state.thread_id = thread_id            # it is manadatory to resume the chat where it left
            state.message_history = []
            state.uploader_key += 1                # just for clean ui
            state.pop("doc_loaded", None)

            message = chatbot.get_state(config= {"configurable" : {"thread_id" : thread_id}})
            messages = message.values.get("messages", [])  # If thread_id not present in State Memory, then no msg []

            # Load all msg from State Memory to message_history       
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    role = "user"
                elif isinstance(msg, AIMessage) and msg.content:  # some aimessage represent tool calls,then content is null there
                    role = "ai"
                else:
                    continue
                state.message_history.append(
                    {"role":role, "content":msg.content}
                    )

# Function 3
def generate_title(user_input):

    title_prompt = f"""
            You are a title generator.
            Based on the user's message below, generate a concise chat title.
            Rules:
            - Maximum 3 to 4 words
            - Use title case
            - No quotes or punctuations
            - Capture the core topic only
            User message:
            {user_input}
            """
    return title_llm.invoke(title_prompt).content.strip()

# Function 4
def load_file(upload_file):
    if "thread_id" not in state:
        state.thread_id = str(uuid4())                          # generate new thread_id after doc upload

        with st.spinner("Document is processing..."):
            
            temp_path = f"temp_{state.thread_id}.pdf"            # For multiple user's conflict
            with open(temp_path, "wb") as f:                     # Saving the file as temp.pdf
                f.write(upload_file.getbuffer())                 # Memory efficient

            embed_model = load_embed()
            get_retriever(temp_path, state.thread_id, embed_model)  # retriever object create

            state.doc_loaded = True
            os.remove(temp_path)                                 # Delete temporary pdf