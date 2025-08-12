import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
VECTORSTORE_DIR = str(BASE_DIR / "vectorstore")
UPLOAD_DIR = str(BASE_DIR / "uploaded_docs")
LOGS_DIR = str(BASE_DIR / "logs")

os.makedirs(VECTORSTORE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "thenlper/gte-large")  
RERANK_MODEL_NAME = os.getenv("RERANK_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")  

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3-70b-8192") 

#KEY for Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
