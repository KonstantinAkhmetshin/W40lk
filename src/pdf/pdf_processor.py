from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import os

# PDF text extraction and processing
def process_pdf():
    pdf_path = os.environ.get("PDF_PATH")
    print("pdf path: ", pdf_path)
    start_time = time.time()
    
    print("loading pdf...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    load_time = time.time() - start_time
    print(f"PDF loaded in {load_time:.2f} seconds")
    
    print("splitting pdf...")
    split_start_time = time.time()
    text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )
    texts = text_splitter.split_documents(documents)
    
    split_time = time.time() - split_start_time
    print(f"PDF split in {split_time:.2f} seconds")
    
    total_time = time.time() - start_time
    print(f"Total processing time: {total_time:.2f} seconds")
    
    return texts