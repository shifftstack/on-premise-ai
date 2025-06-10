import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from pypdf import PdfReader
from docx import Document as DocxDocument

CHROMA_COLLECTION = "documents"
CHROMA_PATH = "chromadb_store"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)

ollama_embeddings = OllamaEmbeddings(model="llama4")


def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(filepath):
    doc = DocxDocument(filepath)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text(filepath):
    if filepath.lower().endswith(".pdf"):
        return extract_text_from_pdf(filepath)
    elif filepath.lower().endswith(".docx"):
        return extract_text_from_docx(filepath)
    else:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def ingest_document(filepath, doc_id=None):
    text = extract_text(filepath)
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    chunks = splitter.split_text(text)
    metadatas = [{"filename": os.path.basename(filepath), "chunk": i} for i in range(len(chunks))]
    ids = [f"{doc_id or os.path.basename(filepath)}_{i}" for i in range(len(chunks))]
    embeddings = ollama_embeddings.embed_documents(chunks)
    collection.add(documents=chunks, metadatas=metadatas, ids=ids, embeddings=embeddings)
    return len(chunks) 