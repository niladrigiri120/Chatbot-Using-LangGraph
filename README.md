📄 Chatterly - RAG based AI Chatbot with Observability

A production-structured Streamlit-based AI chatbot powered by Retrieval-Augmented Generation (RAG), LangGraph orchestration, and full observability using LangSmith.

This application enables intelligent document querying with structured workflow control, real-time tracing, and automatic conversation title generation.

🚀 Features :

    📎 Upload and analyze PDF documents
    🔎 Semantic search using FAISS vector store
    🧠 Retrieval-Augmented Generation (RAG) pipeline
    🔄 LangGraph-based workflow orchestration
    📊 LangSmith observability and trace monitoring
    🏷 Automatic conversation title generation
    💬 ChatGPT-style minimal UI
    🧵 Thread-based session management
    ⚡ Cached embeddings and model loading
    🔐 Secure API key handling

🏗 Project Architecture :

    project/
    │
    ├── app.py
    │
    ├── frontend/
    │   ├── html.py
    │   ├── streaming.py
    │   └── utility.py
    │
    ├── backend/
    │   ├── database.py
    │   ├── model.py
    │   ├── rag.py
    │   ├── state.py
    │   └── tools.py
    │
    ├── .env
    ├── requirements.txt
    └── README.md

⚙️ Tech Stack :

    Streamlit – UI framework
    LangChain – LLM integration
    LangGraph – Stateful workflow orchestration
    FAISS – Vector similarity search
    Sentence Transformers – Embedding models
    Groq API – High-speed LLM inference
    LangSmith – Observability & execution tracing
    SQLite – Thread checkpointing

🧠 System Workflow :

    1️⃣ Document Processing

    PDF is uploaded.
    Document is chunked and embedded.
    Embeddings are stored in FAISS.

    2️⃣ Query Handling

    User query triggers retriever.
    Relevant chunks are injected as context.
    LangGraph manages message flow.
    LLM generates grounded response.

    3️⃣ Observability (LangSmith)

    Every RAG call is traced.
    Execution graphs are monitored.
    Token usage & latency tracked.
    Debugging supported through trace visualization.

    4️⃣ Automatic Title Generation

    On initial user query:
    A short contextual title is generated.
    Title is stored per thread.
    Displayed in sidebar for session clarity.

📊 Observability with LangSmith :

    LangSmith is integrated to provide:
    Execution tracing
    Prompt inspection
    Latency analysis
    Token usage tracking
    Error debugging
    Environment variables required:

🔐 Environment Setup :

    Create a .env file:

    GROQ_API_KEY=your_groq_key
    ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key

    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT = 'https://api.smith.langchain.com'
    LANGSMITH_API_KEY=your_langsmith_key
    LANGSMITH_PROJECT=rag-chatbot

Add .env to .gitignore.

📦 Installation :

``git clone <your-repo>
cd project
pip install -r requirements.txt
``

▶ Run the App

``streamlit run app.py``

🧩 Design Principles :

    Clear separation of frontend and backend
    Cached heavy resources using @st.cache_resource
    Thread-based session architecture
    Modular RAG pipeline
    Observability-first design
    Secure secret management
    Scalable folder structure

📌 Future Enhancements :

    Persistent vector database
    Multi-document indexing
    User authentication
    Deployment with CI/CD
    Usage analytics dashboard
    Advanced memory summarization

👤 Author :

Niladri Giri

Data Scientist, AI/ML Engineer, RAG Systems, LLM Applications