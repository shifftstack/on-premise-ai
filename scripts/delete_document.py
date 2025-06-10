import sqlite3
import sys
import os

DB_PATH = "../onpremiseai.db"
UPLOAD_DIR = "../backend/app/uploaded_docs"

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_document.py filename")
        return
    filename = sys.argv[1]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM documents WHERE filename = ?", (filename,))
    conn.commit()
    if c.rowcount:
        print(f"Document {filename} deleted from DB.")
        file_path = os.path.join(UPLOAD_DIR, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} removed from disk.")
        else:
            print(f"File {file_path} not found on disk.")
    else:
        print("Document not found in DB.")
    conn.close()

if __name__ == "__main__":
    main() 