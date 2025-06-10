from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from pydantic import BaseModel
from app.services import rag, ollama_client

router = APIRouter(prefix="/chat", tags=["chat"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []

@router.post("/query", response_model=ChatResponse)
def chat_query(request: ChatRequest, user=Depends(get_current_user)):
    contexts, metadatas = rag.retrieve_context(request.message)
    context_str = "\n".join(contexts)
    prompt = f"Context:\n{context_str}\n\nQuestion: {request.message}\nAnswer:"
    answer = ollama_client.generate_completion(prompt)
    sources = [meta["filename"] for meta in metadatas]
    return ChatResponse(answer=answer, sources=sources) 