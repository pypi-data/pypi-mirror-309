import streamlit as st
from .summarizer import run_summarizer
from .rag_chatbot import run_rag_chatbot
from .langgraph_agents import run_langgraph_agents

def main():
    st.set_page_config(page_title="Learn GenAI", page_icon="🧠", layout="wide")
    st.title("Learn Generative AI")

    use_case = st.sidebar.selectbox(
        "Select a use case",
        ["Summarizer", "RAG Chatbot", "LangGraph Agents"]
    )

    if use_case == "Summarizer":
        run_summarizer()
    elif use_case == "RAG Chatbot":
        run_rag_chatbot()
    elif use_case == "LangGraph Agents":
        run_langgraph_agents()

if __name__ == "__main__":
    main()
