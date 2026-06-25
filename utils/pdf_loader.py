from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import hashlib

def get_cache_path(pdf_paths: list[str]) -> str:
    key = "_".join(sorted(pdf_paths))
    hash_key = hashlib.md5(key.encode()).hexdigest()
    return f"vectorstore_cache/{hash_key}"

def load_pdfs(pdf_paths: list[str]):
    docs = []
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs

def build_vectorstore(pdf_paths: list[str]):
    cache_path = get_cache_path(pdf_paths)
    embeddings = OpenAIEmbeddings()
    
    if os.path.exists(cache_path):
        return FAISS.load_local(cache_path, embeddings, allow_dangerous_deserialization=True)
    
    docs = load_pdfs(pdf_paths)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    os.makedirs(cache_path, exist_ok=True)
    vectorstore.save_local(cache_path)
    
    return vectorstore

def get_retriever(pdf_paths: list[str]):
    vectorstore = build_vectorstore(pdf_paths)
    return vectorstore.as_retriever(search_kwargs={"k": 4})