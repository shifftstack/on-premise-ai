import sqlite3

DB_PATH = "onpremiseai.db"

def log_action(action, actor, target=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO audit_logs (action, actor, target) VALUES (?, ?, ?)",
        (action, actor, target)
    )
    conn.commit()
    conn.close() 