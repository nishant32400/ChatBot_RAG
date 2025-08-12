from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os, shutil, time, json
from document_processor import process_and_store_documents
from rag_pipeline import retrieve_and_generate
from config import UPLOAD_DIR, LOGS_DIR

app = FastAPI(title="RAG Study Assistant API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-docs/")
async def upload_docs(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    for f in files:
        dest = os.path.join(UPLOAD_DIR, f.filename)
        with open(dest, "wb") as buffer:
            shutil.copyfileobj(f.file, buffer)
    return process_and_store_documents(UPLOAD_DIR)

@app.get("/ask/")
async def ask_question(q: str):
    result = retrieve_and_generate(q)
    
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        log_path = os.path.join(LOGS_DIR, "interactions.jsonl")
        payload = {"ts": time.time(), "query": q, **result}
        with open(log_path, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return result
