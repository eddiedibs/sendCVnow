from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from src.data import constants as const

def vector_embed(data):
    # Split and chunk 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    # Add to vector database
    vector_db = Chroma.from_documents(
        documents=chunks, 
        embedding=OllamaEmbeddings(base_url=f"{const.OLLAMA_HOST}:{const.OLLAMA_PORT}", model="nomic-embed-text",show_progress=True),
        collection_name="local-rag"
    )

    return vector_db

