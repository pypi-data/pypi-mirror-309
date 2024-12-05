import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def run_summarizer():
    st.header("Text Summarizer")
    
    text = st.text_area("Enter the text to summarize:", height=200)
    
    if st.button("Summarize"):
        if text:
            with st.spinner("Summarizing..."):
                # Inizializza il modello Ollama
                llm = Ollama(model="llama3.2:3b")  # Cambia in "llama3.2:3b" se necessario
                
                # Crea un text splitter
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len
                )
                
                # Dividi il testo in chunks
                texts = text_splitter.split_text(text)
                
                # Crea documenti dai chunks
                docs = [Document(page_content=t) for t in texts]
                
                # Carica la chain di summarization
                chain = load_summarize_chain(llm, chain_type="map_reduce")
                
                # Esegui la summarization
                summary = chain.run(docs)
                
                st.subheader("Summary:")
                st.write(summary)
        else:
            st.warning("Please enter some text to summarize.")
