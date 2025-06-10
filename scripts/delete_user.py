import sqlite3
import sys

DB_PATH = "../onpremiseai.db"

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_user.py email")
        return
    email = sys.argv[1]
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    if c.rowcount:
        print(f"User {email} deleted.")
    else:
        print("User not found.")
    conn.close()

if __name__ == "__main__":
    main() 