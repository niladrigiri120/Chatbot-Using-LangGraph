# -------------------- Importing Libraries --------------------
import streamlit as st
from uuid import uuid4
from langchain_core.messages import HumanMessage

from backend.state import build_graph
from backend.database import create_table, load_table, save_table, update_table

from frontend.html import sidebar_ui
from frontend.utility import show_welcome, conversation_loader, generate_title, load_file
from frontend.streaming import user_streaming, ai_streaming

chatbot = build_graph()

#--------------------- Session State --------------------
state = st.session_state

if "message_history" not in state:
    state.message_history = []

if "id_history" not in state:
    create_table()
    state.id_history = load_table()  # load existing data from database

if "uploader_key" not in state:
    state.uploader_key = 0

#--------------------- Sidebar --------------------
with st.sidebar:
    sidebar_ui()

    if st.button("📝 New Chat"):
        state.pop("thread_id", None)             # Remove thread_id from session
        state.message_history = []               # Remove the messages from history
        state.uploader_key += 1
        state.pop("doc_loaded", None)

    upload_file = st.file_uploader("Upload PDF", type= ["pdf"], key= state.uploader_key, label_visibility="collapsed")

    # Create retriever only once
    if upload_file and "doc_loaded" not in state :
        load_file(upload_file)

    if "doc_loaded" in state:
        st.success("📄 Document Loaded")

    # Sidebar Header
    st.header("Recent Conversations")
    conversation_loader(chatbot)

#-------------------- Welcome Message -------------------
show_welcome()

#--------------------- Display Conversations --------------------
for msg in state.message_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#-------------------- User Input Area ---------------------------

user_input = st.chat_input("Type your message...")

if user_input and user_input.strip():

    if not state.message_history:
        title = generate_title(user_input)            # Generate Title

        if "thread_id" not in state:
            state.thread_id = str(uuid4())

        save_table(state.thread_id, title)            # save id, title into db
   
    update_table(state.thread_id)                     # update past conversation and show on top
    state.id_history = load_table()                   # load the sidebar buttons immediately

    
    # ------------ Show user input -------------
    with st.chat_message("user"):
        user_streaming(user_input)

    message = {"messages" : [HumanMessage(content= user_input)]}

    # ----------- Show ai response ------------
    with st.chat_message("ai"):
        ai_streaming(message, chatbot)
