import streamlit as st
import os

from utils.pdf_loader import load_pdf
from utils.vector_store import create_vector_store
from utils.chatbot import get_answer

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}



.stApp {
    background:
    linear-gradient(
        rgba(8, 10, 25, 0.82),
        rgba(12, 15, 35, 0.88)
    ),
    url("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=2070&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}


header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    padding-top: 2rem;
}


section[data-testid="stSidebar"] {
    background: rgba(15, 18, 40, 0.92);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: white;
}


.hero-section {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius: 30px;
    padding: 45px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    margin-bottom: 30px;
}

.main-title {
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-bottom: 12px;
}

.main-subtitle {
    color: #D1D5DB;
    font-size: 18px;
    line-height: 1.8;
}


.card {
    background: rgba(255,255,255,0.10);
    backdrop-filter: blur(16px);
    border-radius: 24px;
    padding: 30px;
    min-height: 260px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: 0.3s ease;
}

.card:hover {
    transform: translateY(-6px);
    border: 1px solid rgba(108,99,255,0.35);
    box-shadow: 0 15px 35px rgba(108,99,255,0.22);
}

.card-icon {
    font-size: 46px;
    margin-bottom: 20px;
}

.card-title {
    color: white;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 15px;
}

.card-text {
    color: #E5E7EB;
    font-size: 15px;
    line-height: 1.9;
}


[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.08);
    border: 2px dashed rgba(255,255,255,0.18);
    border-radius: 22px;
    padding: 20px;
}


.success-box {
    background: rgba(46,196,182,0.12);
    border: 1px solid rgba(46,196,182,0.25);
    color: #D1FAE5;
    padding: 18px;
    border-radius: 18px;
    font-weight: 500;
    margin-top: 18px;
}

.chat-wrapper {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 30px;
    margin-top: 35px;
    border: 1px solid rgba(255,255,255,0.08);
}

.chat-heading {
    color: white;
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 8px;
}

.chat-sub {
    color: #D1D5DB;
    margin-bottom: 25px;
}

.user-message {
    background: linear-gradient(135deg, #6C63FF, #7C72FF);
    padding: 18px;
    border-radius: 22px 22px 6px 22px;
    color: white;
    margin-left: 25%;
    margin-top: 18px;
    box-shadow: 0 8px 18px rgba(108,99,255,0.28);
}

.bot-message {
    background: rgba(255,255,255,0.94);
    padding: 18px;
    border-radius: 22px 22px 22px 6px;
    color: #111827;
    margin-right: 25%;
    margin-top: 18px;
    box-shadow: 0 8px 18px rgba(0,0,0,0.08);
    border-left: 4px solid #2EC4B6;
}


[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.10);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

[data-testid="stChatInput"] textarea {
    color: white !important;
    font-size: 16px !important;
}

div[data-testid="stMarkdownContainer"] p {
    margin-bottom: 0px;
}

</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

with st.sidebar:

    st.markdown("""
    <h1 style='text-align:center;'>
    AI Assistant
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Company PDF",
        type=["pdf"]
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.image(
        "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
        width=220
    )


st.markdown("""
<div class="hero-section">

<div class="main-title">
Enterprise AI Knowledge Assistant
</div>

<div class="main-subtitle">
Transform enterprise documents into an intelligent AI-powered knowledge system.
Upload PDFs, retrieve contextual insights instantly, and interact with your data using a premium conversational interface.
</div>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">

    <div class="card-title">
    Smart Search
    </div>

    <div class="card-text">
    Search through enterprise PDFs intelligently using semantic AI retrieval and contextual document understanding.
    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">


    <div class="card-title">
    Instant Responses
    </div>

    <div class="card-text">
    Ask questions and receive accurate AI-generated responses from your uploaded knowledge base.
    </div>

    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">


    <div class="card-title">
    Enterprise Grade
    </div>

    <div class="card-text">
    Modern architecture with sleek design, scalable workflows, and intelligent enterprise document interaction.
    </div>

    </div>
    """, unsafe_allow_html=True)

if uploaded_file:

    save_path = os.path.join(
        "data/uploaded_pdfs",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown("""
    <div class="success-box">
     PDF uploaded successfully and ready for AI processing.
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Processing document and generating embeddings..."):

        # ==================================================
        # EXISTING BACKEND LOGIC
        # ==================================================
        documents = load_pdf(save_path)

        vectorstore = create_vector_store(documents)

        st.session_state.vectorstore = vectorstore


if st.session_state.vectorstore is not None:

    st.markdown("""
    <div class="chat-wrapper">

    <div class="chat-heading">
    💬 AI Knowledge Chat
    </div>

    <div class="chat-sub">
    Ask questions naturally and interact intelligently with your uploaded enterprise documents.
    </div>

    </div>
    """, unsafe_allow_html=True)

    query = st.chat_input(
        "Ask questions about your uploaded document..."
    )

    if query:

        st.session_state.messages.append({
            "role": "user",
            "content": query
        })

        answer = get_answer(
            st.session_state.vectorstore,
            query
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

  
    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(f"""
            <div class="user-message">

            <strong>👤 You</strong>
            <br><br>

            {message["content"]}

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class="bot-message">

            <strong> AI Assistant</strong>
            <br><br>

            {message["content"]}

            </div>
            """, unsafe_allow_html=True)

else:

    st.markdown("""
    <div class="chat-wrapper" style="text-align:center;">

    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
    width="180">

    <br><br>

    <h2 style="color:white;">
    Upload Your PDF To Begin
    </h2>

    <p style="color:#D1D5DB; font-size:16px;">
    Your AI assistant is ready to analyze enterprise documents,
    retrieve insights, and answer questions intelligently.
    </p>

    </div>
    """, unsafe_allow_html=True)