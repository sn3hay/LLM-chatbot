from dotenv import load_dotenv
from langchain.embeddings import HuggingFaceEmbeddings

# Load environment variables (if needed)
load_dotenv()

# Use a Hugging Face embedding model (fast and free)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

text = "Algoritma is a data science school based in Indonesia and Supertype is a data science consultancy with a distributed team of data and analytics engineers."
doc_embeddings = embeddings.embed_documents([text])

print(doc_embeddings)
