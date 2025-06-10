from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from typing import List
import os
import sqlite3
from app.services import ingestion

router = APIRouter(prefix="/documents", tags=["documents"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

UPLOAD_DIR = "uploaded_docs"
DB_PATH = "onpremiseai.db"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    return sqlite3.connect(DB_PATH)

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

@router.post("/upload")
def upload_document(file: UploadFile = File(...), user=Depends(get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    # Ingest into ChromaDB
    num_chunks = ingestion.ingest_document(file_path)
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "INSERT INTO documents (filename, uploader) VALUES (?, ?)",
        (file.filename, user["sub"])
    )
    conn.commit()
    conn.close()
    return {"filename": file.filename, "chunks": num_chunks}

@router.get("/list", response_model=List[dict])
def list_documents(user=Depends(get_current_user)):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT filename, uploader, upload_time FROM documents")
    docs = [
        {"filename": row[0], "uploader": row[1], "upload_time": row[2]} for row in c.fetchall()
    ]
    conn.close()
    return docs 