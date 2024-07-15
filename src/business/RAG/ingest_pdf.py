import os


from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from src.data import constants as const




def ingest_pdf(file_name:str):

    file_location = os.path.join(const.CV_DIR, file_name)
    # Local PDF file uploads
    if file_location:
        loader = UnstructuredPDFLoader(file_path=file_location)
        data = loader.load()
        return data
    else:
        return None