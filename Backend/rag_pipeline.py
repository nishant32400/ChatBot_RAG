from typing import Dict, List, Tuple
import os
import requests
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from sentence_transformers import CrossEncoder
from config import VECTORSTORE_DIR, EMBEDDING_MODEL_NAME, RERANK_MODEL_NAME, LLM_MODEL_NAME, GROQ_API_KEY

def _get_vectorstore() -> Chroma:
    embedding_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    return Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embedding_model
    )

def _rerank(query: str, docs, top_k: int = 6) -> List:

    cross_encoder = CrossEncoder(RERANK_MODEL_NAME)
    pairs = [(query, d.page_content) for d in docs]
    scores = cross_encoder.predict(pairs)

    scored = list(zip(docs, scores))
    scored.sort(key=lambda x: float(x[1]), reverse=True)
    return [d for d, s in scored[:top_k]]

def _call_groq_chat(messages: List[Dict[str, str]]) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env or environment variables.")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": LLM_MODEL_NAME,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": 800
    }
    resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

def retrieve_and_generate(query: str, k: int = 12) -> Dict[str, List[str]]:
    # 1) Retrieve
    vs = _get_vectorstore()
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": k})
    retrieved_docs = retriever.get_relevant_documents(query)
    if not retrieved_docs:
        return {"answer": "I couldn't find anything relevant in the indexed documents. Try uploading PDFs and re-processing.", "sources": []}

    
    reranked = _rerank(query, retrieved_docs, top_k=min(6, len(retrieved_docs)))


    context_blocks = []
    sources: List[str] = []
    for i, d in enumerate(reranked, start=1):
        src = d.metadata.get("source", "Unknown")
        page = d.metadata.get("page", None)
        label = f"{src}" + (f" [page {page}]" if page is not None else "")
        sources.append(label)
        context_blocks.append(f"[#{i}] Source: {label}\n{d.page_content.strip()}")

    context = "\n\n".join(context_blocks)

    system_prompt = (
        "You are a study assistant that answers STRICTLY using the provided context blocks. "
        "Cite sources like [#1], [#2] in your answer where relevant. "
        "If the answer is not in the context, say you don't have enough information."
    )
    user_prompt = f"Question: {query}\n\nContext Blocks:\n{context}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        answer = _call_groq_chat(messages)
    except Exception as e:
        answer = f"LLM call failed: {e}. Please check your GROQ_API_KEY and internet connectivity."
    
    seen = set()
    uniq_sources = []
    for s in sources:
        if s not in seen:
            uniq_sources.append(s); seen.add(s)
    return {"answer": answer, "sources": uniq_sources}
