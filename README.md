AI Study Assistant with (RAG)

A simple end-to-end Retrieval-Augmented Generation chatbot using RAG: upload PDFs → embed & index in Chroma → ask questions → get cited answers.  
Backend: FastAPI + LangChain + Chroma + sentence-transformers + Groq.  
Frontend: Streamlit.

---

## 1) Prerequisites

- **Windows 10/11** with **Python 3.10–3.12**
- **Groq API key**

> ⚠️ The default embedding model `thenlper/gte-large` is ~1.3GB. If you’re on a low-RAM machine, set `EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2` in your `.env` to speed things up (slightly lower quality).

---

## 2) Quick Start
Open **Windows PowerShell** and run these commands step-by-step:

```powershell
cd .\Chatbot_use_ai

python -m venv .venv
.\.venv\Scripts\activate

pip install -r Backend\requirements.txt

Copy-Item Backend\.env.example Backend\.env
# Then open Backend\.env in Notepad and paste your key/value

uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir Backend

.\.venv\Scripts\activate

streamlit run Frontend\app.py
```

Now open the app in your browser at: **http://localhost:8501**

---

## 3) Configuration

Create `Backend/.env`:

```env
# ==== Required ====
GROQ_API_KEY=your_groq_key_here

# ==== Optional (recommended for smaller downloads) ====
# EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
# RERANK_MODEL_NAME=cross-encoder/ms-marco-MiniLM-L-6-v2
# LLM_MODEL_NAME=llama3-70b-8192
```

**Backend:**
- `uploaded_docs/` — PDFs you upload via the UI
- `vectorstore/` — persisted Chroma index
- `logs/` — JSONL logs of Q&A

---

## 4) What’s Included

- **Document ingestion:** `PyPDFDirectoryLoader` → `RecursiveCharacterTextSplitter` (512/16 with `cl100k_base`)
- **Embeddings:** `SentenceTransformerEmbeddings` (default `thenlper/gte-large`)
- **Vector DB:** **Chroma** (persisted on disk)
- **Retrieval:** top-12 similarity search
- **Re-ranking:** Cross-encoder (`ms-marco-MiniLM-L-6-v2`) → top-6
- **Generation:** Groq Chat Completions (default `mixtral-8x7b-32768`)
- **Citations:** Sources shown; use [#1], [#2] in answers
- **Logging:** JSONL for audits/analytics


## 5) Project Structure

```
Chatbot_use_ai/
├── Backend/
│   ├── main.py
│   ├── config.py
│   ├── document_processor.py
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── uploaded_docs/
│   ├── vectorstore/
│   └── logs/
└── Frontend/
    └── app.py
```

---

## 7) API (if you want to test with curl/Postman)

- **Upload PDFs**
  ```bash
  curl -F "files=@/path/to/file.pdf" http://localhost:8000/upload-docs/
  ```
- **Ask question**
  ```bash
  curl "http://localhost:8000/ask/?q=What is chapter 1 about?"
  ```

---
