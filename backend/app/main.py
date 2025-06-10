from fastapi import FastAPI
from app.api import auth, chat, documents, admin

app = FastAPI()

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(admin.router)

@app.get("/health")
def health_check():
    return {"status": "ok"} 