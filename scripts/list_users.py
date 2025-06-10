import sqlite3

DB_PATH = "../onpremiseai.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, email, is_admin FROM users")
    users = c.fetchall()
    print("ID\tEmail\t\tAdmin")
    for user in users:
        print(f"{user[0]}\t{user[1]}\t{bool(user[2])}")
    conn.close()

if __name__ == "__main__":
    main() 