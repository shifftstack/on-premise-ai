# OnPremiseAI

See PRODUCT_DESIGN.md, TECHNICAL_DESIGN.md, and IMPLEMENTATION_PLAN.md for design and implementation details.

## Quickstart

1. **Clone the repo**
2. **Install Docker and Docker Compose**
   - [Docker Install Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Install Guide](https://docs.docker.com/compose/install/)
3. **Initialize the database:**
   ```bash
   python scripts/init_db.py
   python scripts/add_audit_log_table.py
   ```
4. **Start all services (Ollama, ChromaDB, SQLite, Backend, Frontend):**
   ```bash
   docker-compose up --build
   ```
   - This will automatically start:
     - **Ollama** (Llama 4 model server)
     - **ChromaDB** (vector database)
     - **SQLite** (local file, no server needed)
     - **Backend** (FastAPI)
     - **Frontend** (React)
5. **Add your first user (admin):**
   ```bash
   python scripts/add_user.py admin@example.com yourpassword --admin
   ```
6. **Access the app:**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000/docs](http://localhost:8000/docs)

## Manual Installation (Advanced/Custom)
- **Ollama:** [https://ollama.com/download](https://ollama.com/download)
- **ChromaDB:** [https://docs.trychroma.com/](https://docs.trychroma.com/)
- **SQLite:** [https://www.sqlite.org/download.html](https://www.sqlite.org/download.html) (CLI tools, not needed for Python usage)
- **Python dependencies:**
  ```bash
  pip install -r backend/requirements.txt
  ```
- **Frontend dependencies:**
  ```bash
  cd frontend && npm install
  ```

## User Guide
- **Register/Login:** Use the web UI to register or log in.
- **Chat:** Ask questions in the chat window.
- **Upload Documents:** Upload PDFs, DOCX, or TXT files for ingestion.
- **View Documents:** See all uploaded documents in the document management panel.

## Admin Guide
- **User Management:** Admins can list and delete users in the admin panel.
- **Audit Logs:**
  - All admin actions are logged in the audit log (SQLite).
  - Export logs: `python scripts/export_audit_logs.py`
- **Backup/Restore:**
  - Backup: `bash scripts/backup.sh`
  - Restore: `bash scripts/restore.sh <backup_dir>`

## Maintenance
- All database and compliance operations are handled via scripts in the `scripts/` directory.
- For advanced maintenance, see the scripts and design docs.

## Compliance
- All data is stored locally (SQLite, ChromaDB, uploaded files).
- Audit logs are exportable for compliance.

---

For more, see the design docs and implementation plan in this repo.

## Database & Maintenance

- Uses SQLite for all persistent storage (users, documents, etc.)
- All database setup and maintenance is handled via scripts in the `scripts/` directory
- To initialize the database, run:

```bash
python scripts/init_db.py
```

- For backup/restore, see `scripts/backup.sh` and `scripts/restore.sh` 