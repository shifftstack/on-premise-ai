import sqlite3
import sys
from app.core.security import get_password_hash

DB_PATH = "../onpremiseai.db"

def main():
    if len(sys.argv) < 3:
        print("Usage: python add_user.py email password [--admin]")
        return
    email = sys.argv[1]
    password = sys.argv[2]
    is_admin = 0
    if len(sys.argv) > 3 and sys.argv[3] == "--admin":
        is_admin = 1
    hashed = get_password_hash(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (email, hashed_password, is_admin) VALUES (?, ?, ?)",
            (email, hashed, is_admin)
        )
        conn.commit()
        print(f"User {email} added. Admin: {bool(is_admin)}")
    except sqlite3.IntegrityError:
        print("User already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 