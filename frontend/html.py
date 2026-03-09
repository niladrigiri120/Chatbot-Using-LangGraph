import streamlit as st

def sidebar_ui():
    st.markdown("""
    <h1 style="
        text-align:center;
        margin-top:0px;
        margin-bottom:30px;
    ">
        Chatterly ✨
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    /* Hide drag and drop text */
    div[data-testid="stFileUploader"] > div > div:nth-child(1) {
        display: none;
    }

    /* Hide file size & type text */
    div[data-testid="stFileUploader"] small {
        display: none;
    }

    /* Hide uploaded file name */
    div[data-testid="stFileUploaderFile"] {
        display: none !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>

    /* Sidebar chat buttons */
    div.stButton > button {
        border-radius: 10px;
        transition: 0.2s ease;
    }

    /* Hover effect */
    div.stButton > button:hover {
        background-color: #2a2f3a;
    }

    /* Remove ugly focus outline */
    div.stButton > button:focus {
        box-shadow: none;
    }

    </style>
    """, unsafe_allow_html=True)