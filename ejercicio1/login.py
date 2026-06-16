import sqlite3
import bcrypt
import os
from pydantic import BaseModel, EmailStr

DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = "users.db"

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr

def get_user(username: str, password: str) -> dict:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return {"status": "ok", "user": {"id": user[0], "username": user[1]}}
    return {"status": "error", "message": "Invalid credentials"}

def reset_password(user_id: int, new_pass: str) -> bool:
    hashed_password = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "UPDATE users SET password=? WHERE id=?",
            (hashed_password, user_id)
        )
        conn.commit()
    return True

def create_user(username: str, password: str, email: str) -> dict:
    try:
        UserCreate(username=username, password=password, email=email)
    except ValueError as e:
        return {"status": "error", "message": str(e)}

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email)
        )
        conn.commit()
    return {"status": "created", "username": username}