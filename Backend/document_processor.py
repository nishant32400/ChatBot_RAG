from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from config import VECTORSTORE_DIR, UPLOAD_DIR, EMBEDDING_MODEL_NAME
from typing import Dict

def process_and_store_documents(upload_dir: str = UPLOAD_DIR) -> Dict[str, str]:
   
    loader = PyPDFDirectoryLoader(upload_dir)
    documents = loader.load()
    if not documents:
        return {"status": "error", "message": "No PDFs found to process. Please upload files."}

    
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        encoding_name='cl100k_base',
        chunk_size=512,
        chunk_overlap=16
    )
    chunks = text_splitter.split_documents(documents)

    embedding_model = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

  
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=VECTORSTORE_DIR
    )
    vectorstore.persist()
    return {"status": "success", "message": f"Processed {len(documents)} document(s) → {len(chunks)} chunks. Ready to chat!"}
