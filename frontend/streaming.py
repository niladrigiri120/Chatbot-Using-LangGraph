import time
import streamlit as st
from langchain_core.messages import AIMessage

state = st.session_state

# Function 1
def user_streaming(user_input):
    st.markdown(user_input)
    state.message_history.append({"role" : "user", "content" : user_input})

# Function 2
def ai_streaming(message, chatbot):
    with st.spinner("Generating response..."):
            
        CONFIG = {"configurable" : {"thread_id" : state.thread_id},
                  "run_name" : "Chatterly"}
            
        message_placeholder = st.empty()  # it stores content one at a time
        ai_content = ""
        tool_use = False

        for chunk, metadata in chatbot.stream(message, config= CONFIG, stream_mode= "messages"):

            if metadata.get("langgraph_node") == "tools" and not tool_use:
                st.info(f"Using tool...")
                tool_use = True

            if isinstance(chunk, AIMessage) and chunk.content.strip() :
                ai_content += chunk.content
                message_placeholder.markdown(ai_content)
                time.sleep(0.03)                                  # delaying effect
    message_placeholder.markdown(ai_content)
    
    state.message_history.append({"role" : "ai", "content" : ai_content})
