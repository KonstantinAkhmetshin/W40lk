from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import os

# Global variable to store the vector store instance
vectorstore = None

def get_persist_directory():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    persist_directory = os.path.abspath(os.path.join(current_dir,  "..", "vector_storage"))
    print("vector storage directory: ", persist_directory)
    return persist_directory

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        print("creating vector store")
        persist_directory = get_persist_directory()
        embeddings = get_embeddings()
        vectorstore = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        print("vector store created")
    return vectorstore


def add_texts(texts):
    print("adding texts to vector store")
    global vectorstore
    vectorstore = get_vectorstore()
    vectorstore.add_documents(texts)
    vectorstore.persist()
    print("texts added and vector store saved")

def search_similar(query, k=4):
    return get_vectorstore().similarity_search(query, k=k)

def verify_storage_exists_and_empty():
    persist_directory = get_persist_directory()
    
    # Check if the directory exists
    if not os.path.exists(persist_directory):
        print("Vector storage directory does not exist.")
        return False
    
    # Check if the directory is empty
    if not os.listdir(persist_directory):
        print("Vector storage directory is empty.")
        return True
    
    # If we reach here, the directory exists and is not empty
    print("Vector storage exists and contains data.")
    return False
