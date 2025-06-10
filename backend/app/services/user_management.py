import sqlite3
from app.models.user import UserCreate, UserInDB, UserResponse
from app.core.security import get_password_hash, verify_password
from typing import Optional

DB_PATH = "onpremiseai.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def create_user(user: UserCreate) -> UserResponse:
    conn = get_db()
    c = conn.cursor()
    try:
        hashed = get_password_hash(user.password)
        c.execute(
            "INSERT INTO users (email, hashed_password, is_admin) VALUES (?, ?, ?)",
            (user.email, hashed, int(user.is_admin))
        )
        conn.commit()
        user_id = c.lastrowid
        return UserResponse(id=user_id, email=user.email, is_admin=user.is_admin)
    except sqlite3.IntegrityError:
        raise ValueError("User already exists")
    finally:
        conn.close()

def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, email, hashed_password, is_admin FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    id, email, hashed_password, is_admin = row
    if not verify_password(password, hashed_password):
        return None
    return UserInDB(id=id, email=email, hashed_password=hashed_password, is_admin=bool(is_admin))

def get_user(email: str) -> Optional[UserInDB]:
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, email, hashed_password, is_admin FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    id, email, hashed_password, is_admin = row
    return UserInDB(id=id, email=email, hashed_password=hashed_password, is_admin=bool(is_admin))

def list_users() -> list:
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, email, is_admin FROM users")
    users = [UserResponse(id=row[0], email=row[1], is_admin=bool(row[2])) for row in c.fetchall()]
    conn.close()
    return users

def delete_user(email: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close() 