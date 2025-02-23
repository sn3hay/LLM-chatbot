import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import os
# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="pdf_docs")

PDF_PATH = "./pdfs/llm-chatbot.pdf"

def extract_text_from_pdf(pdf_path=PDF_PATH):
    """Extracts text from the given PDF file in the directory."""
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")
    
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def store_text_in_chroma(text):
    """Splits text into chunks and stores in ChromaDB."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[str(i)],
            documents=[chunk]
        )

def retrieve_relevant_text(query, k=3):
    """Retrieves relevant text from ChromaDB based on query."""
    results = collection.query(
        query_texts=[query],
        n_results=k
    )
    return " ".join(results["documents"][0]) if results["documents"] else ""
