import sqlite3
import csv

DB_PATH = "../onpremiseai.db"
EXPORT_PATH = "../audit_logs_export.csv"

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, action, actor, target, timestamp FROM audit_logs ORDER BY timestamp DESC")
    rows = c.fetchall()
    with open(EXPORT_PATH, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'action', 'actor', 'target', 'timestamp'])
        writer.writerows(rows)
    print(f"Exported {len(rows)} audit logs to {EXPORT_PATH}")
    conn.close()

if __name__ == "__main__":
    main() 