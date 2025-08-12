import streamlit as st
import requests

st.set_page_config(page_title="AI Study Assistant (RAG)", page_icon="📚", layout="wide")

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.title("📚 AI Study Assistant (RAG)")

with st.sidebar:
    st.header("Upload Study Material")
    uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    if st.button("Process Documents", use_container_width=True):
        if not uploaded_files:
            st.warning("Please upload at least one PDF first.")
        else:
            files = [("files", (f.name, f, "application/pdf")) for f in uploaded_files]
            try:
                res = requests.post(f"{BACKEND_URL}/upload-docs/", files=files, timeout=120)
                res.raise_for_status()
                st.success(res.json().get("message", "Processed!"))
            except Exception as e:
                st.error(f"Processing failed: {e}")

st.header("Ask a Question")
query = st.text_input("Type your question here...")

col1, col2 = st.columns([1, 3])
with col1:
    ask = st.button("Get Answer", use_container_width=True)
with col2:
    st.caption("Tip: Ask specific questions like 'Summarize chapter 2' or 'Create a quiz from chapter 1'.")

if ask and query.strip():
    try:
        res = requests.get(f"{BACKEND_URL}/ask/", params={"q": query}, timeout=120)
        res.raise_for_status()
        data = res.json()
        st.subheader("Answer")
        st.write(data.get("answer", ""))
        st.subheader("Sources")
        for src in data.get("sources", []):
            st.markdown(f"- {src}")
    except Exception as e:
        st.error(f"Error: {e}")
