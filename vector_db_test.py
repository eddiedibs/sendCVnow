#!/home/edd1e/scripts/projs/portfolio_stuff/sendCVNow/venv/bin/python3

from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
import sys
import time

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from src.data import constants as const




def ingest_pdf(location_path):

    file_location = location_path
    # Local PDF file uploads
    if file_location:
        loader = UnstructuredPDFLoader(file_path=file_location)
        data = loader.load()
        return data
    else:
        return None

def vector_embed(data=None):

    CONN_STRING = "postgresql+psycopg2://postgres:123456@localhost:5422/vector_db"
    COLLECTION_NAME = "state_of_union_vectors"
    # Split and chunk 
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    # chunks = text_splitter.split_documents(data)

    # Add to vector database
    vector_db = PGVector(
        # documents=chunks, 
        embeddings=OllamaEmbeddings(base_url=f"{const.OLLAMA_HOST}:{const.OLLAMA_PORT}", model="nomic-embed-text",show_progress=True),
        collection_name=COLLECTION_NAME,
        # connection_string=CONN_STRING,
        connection=CONN_STRING,
        use_jsonb=True,
    )

    

    return vector_db


def retrieve_data(llm_model, vector_db):
    # LLM from Ollama
    # local_model = "mistral"
    llm = ChatOllama(model=llm_model, base_url=f"{const.OLLAMA_HOST}:{const.OLLAMA_PORT}")

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template= const.OLLAMA_INIT_INSTRUCT + """{question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llm,
        prompt=QUERY_PROMPT
    )

    # RAG prompt
    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(sys.argv[1])

# data = ingest_pdf("/home/edd1e/scripts/projs/portfolio_stuff/sendCVNow/src/CVs/johnnytest-cv_english-a723acd5-5376-4bd3-b3a0-21dddff13312.pdf")
# print(f"PDF DATA: {data}")
start_time = time.time()  # or time.perf_counter()
vector_db = vector_embed()
print(f"VECTOR_DB:: \n\n\n {vector_db}")
retrieve_result = retrieve_data("llama3:instruct", vector_db)
print(f"RESULT:: \n\n\n {retrieve_result}")
end_time = time.time()  # or time.perf_counter()
execution_time = end_time - start_time
print(f"FINISHED IN: {execution_time}")



