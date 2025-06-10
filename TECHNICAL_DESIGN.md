# Technical Design Document

---

## Architecture Overview

- **Frontend:** HTML/React (chat, admin panel)
- **Backend:** FastAPI (Python)
- **RAG Pipeline:** LangChain (Python)
- **LLM:** Ollama (Llama 4, local)
- **Vector DB:** ChromaDB (local)
- **Persistence:** SQLite (all data, managed via scripts)
- **Deployment:** Docker, docker-compose

---

## Component Diagram

```mermaid
graph TD
  subgraph User
    A[Web Browser]
  end
  subgraph On-Prem Server
    B[Frontend (HTML/React)]
    C[FastAPI Backend]
    D[LangChain RAG Pipeline]
    E[Ollama (Llama 4)]
    F[ChromaDB (Vector DB)]
    G[Admin Panel]
    H[SQLite DB]
  end
  A-->|HTTPS|B
  B-->|REST/WebSocket|C
  C-->|Python API|D
  D-->|REST|E
  D-->|Python API|F
  C-->|Python API|G
  C-->|SQL|H
```

---

## Data Flow

1. **Document Ingestion**
   - Admin uploads documents via web UI.
   - Backend processes, chunks, and embeds documents using LangChain + Llama 4.
   - Embeddings and metadata stored in ChromaDB.
   - **Document metadata and user info stored in SQLite.**

2. **User Query**
   - User submits question via chat UI.
   - Backend embeds query, retrieves relevant chunks from ChromaDB.
   - Context + query sent to Llama 4 via Ollama for answer.
   - Answer and sources returned to user.

3. **Admin Actions**
   - User management, document management, logs, and model controls via admin panel.
   - All actions logged for audit (in SQLite).
   - **All database and compliance operations are script-driven.**

---

## Security

- JWT/OAuth2 authentication.
- Role-based access (admin/user).
- HTTPS enforced.
- All data and models local (SQLite for persistence).
- Audit logs for all admin actions.

---

## Multi-language Support

- UI: i18n-ready (React/HTML).
- Document: Language detection and support in ingestion pipeline.

---

## Compliance

- Configurable data retention/deletion (via scripts on SQLite DB).
- Audit logs.
- No external data transfer.

---

## Deployment

- All components dockerized.
- docker-compose for orchestration.
- Volumes for persistent data (ChromaDB, uploads, logs, SQLite DB).
- Backup/restore scripts.

---

## Implementation Plan

### 1. Backend
- FastAPI app with endpoints for:
  - User authentication (JWT/OAuth2, stored in SQLite)
  - Chat (query/response)
  - Document upload, delete, re-index (metadata in SQLite)
  - Admin actions (user management, logs, model controls)
- Integrate LangChain for RAG pipeline.
- Integrate with Ollama (Llama 4) via REST.
- Integrate with ChromaDB for vector storage.
- **All persistent data in SQLite, managed via scripts.**

### 2. Frontend
- HTML-first, React for chat/admin.
- Responsive, accessible design.
- i18n support.
- Auth flows (login, logout, role-based UI).

### 3. Vector DB
- ChromaDB running as a local service.
- Expose backup/restore endpoints/scripts.

### 4. LLM
- Ollama running Llama 4 locally.
- Health checks and reload endpoints.

### 5. Admin/Maintenance
- Admin panel for all management tasks.
- Logs and monitoring UI.
- Model reload/restart controls.
- **All DB and compliance operations via scripts.**

### 6. Security
- JWT/OAuth2, HTTPS, RBAC.
- Audit logging.

### 7. Compliance
- Data retention/deletion policies (via scripts).
- Audit log export.

### 8. Deployment
- Dockerfiles for backend, frontend, Ollama, ChromaDB.
- docker-compose.yml for orchestration.
- Documentation for setup, backup, restore, and updates.

---

## Extensibility

- Modular backend for future API integrations.
- Plugin system for new document types or business systems.
- API-first design for future external integrations.
- **All persistent data and compliance operations are script-driven for maintainability.** 