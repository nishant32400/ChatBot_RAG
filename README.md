AI Study Assistant with (RAG)

A simple end-to-end Retrieval-Augmented Generation chatbot using RAG: upload PDFs → embed & index in Chroma → ask questions → get cited answers.  
Backend: FastAPI + LangChain + Chroma + sentence-transformers + Groq.  
Frontend: Streamlit.

---

## 1) Prerequisites

- **Windows 10/11** with **Python 3.10–3.12**
- Internet access (to download models & call Groq)
- A **Groq API key**

> ⚠️ The default embedding model `thenlper/gte-large` is ~1.3GB. If you’re on a low-RAM machine, set `EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2` in your `.env` to speed things up (slightly lower quality).

---

## 2) Quick Start (Local)

Open **Windows PowerShell** and run these commands step-by-step:

```powershell
# 0) Unzip the project, then cd into it
cd .\Chatbot_use_ai

# 1) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 2) Install backend dependencies
pip install -r Backend\requirements.txt

# 3) Create a .env file with your keys (in Backend folder)
Copy-Item Backend\.env.example Backend\.env
# Then open Backend\.env in Notepad and paste your key/value

# 4) Start the FastAPI backend (keep this window open)
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir Backend

# 5) Open a NEW PowerShell window (keep backend running) and activate venv again
.\.venv\Scripts\activate

# 6) Run the Streamlit frontend
streamlit run Frontend\app.py
```

Now open the app in your browser at: **http://localhost:8501**

---

## 3) Configuration

Create `Backend/.env` (or set system environment variables):

```env
# ==== Required ====
GROQ_API_KEY=your_groq_key_here

# ==== Optional (recommended for smaller downloads) ====
# EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
# RERANK_MODEL_NAME=cross-encoder/ms-marco-MiniLM-L-6-v2
# LLM_MODEL_NAME=llama3-70b-8192
```

**Where things live (relative to `Backend/`):**
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

---

## 5) Troubleshooting

- **`GROQ_API_KEY is not set`** → Create `Backend/.env` and add `GROQ_API_KEY=...` (or set env var). Restart backend.
- **Slow / OOM on embeddings** → Switch to `all-MiniLM-L6-v2` in `.env`.
- **Model downloads blocked** → Ensure firewall allows `pypi.org` and `huggingface.co`.
- **CORS / 403** → Make sure backend runs at `http://localhost:8000` before launching Streamlit.
- **Index not updating after new PDFs** → Click **Process Documents** again; it re-embeds and persists.

---

## 6) Project Structure

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

## 8) Security Notes

- **Do NOT** hardcode API keys in code or commit `.env` to git.
- Your key is read from environment variables only.
- Logs may contain queries/answers; handle accordingly.
