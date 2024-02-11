from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

import os
import tempfile
from typing import List
# Tqdm is a popular Python library that provides a simple and convenient way to add 
# progress bars to loops and iterable objects. 
from tqdm import tqdm

def create_llm():
    """
    Creata an instance of Zephyr 7B GGUF format LLM using LlamaCpp

    returns:
    - llm: An instance of  Zephyr 7B LLM
    """
    
    # Create llm
    llm = LlamaCpp(
        streaming = True,
        model_path="artifacts//trained_model//zephyr-7b-beta.Q5_K_S.gguf",
        temperature=0.3,
        top_p=0.8,
        verbose=True,
        n_ctx=4096 #Context Length
    )
    return llm
# def create_vector_store(pdf_files: List):

def create_vector_store(text):
    """
    Create In-memory FAISS vector store using uploaded Pdf

    Args:
    - pdf_files(List): PDF file uploaded
    returns:
    - vector_store: In-memory Vector store for further processing at chat app

    """
    vector_store = None

    # Split the file to chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=10)
    text_chunks = text_splitter.split_text(text)
    documents = text_splitter.create_documents(text_chunks)

    # Check if there are any text chunks
    if not documents:
        print("No text chunks found.")
        return None

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                        model_kwargs={'device': 'cpu'})

    # Create vector store and storing document chunks using embedding model
    vector_store = FAISS.from_documents(documents, embedding=embeddings)

    return vector_store

