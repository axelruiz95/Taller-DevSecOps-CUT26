import sqlite3
import os
import bcrypt


DB_PASSWORD = os.getenv("DB_PASSWORD", "default_fallback_or_error_if_not_found")
SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_or_error_if_not_found")
DATABASE = "users.db"

def get_user(username: str, password: str) -> dict:
    
    with sqlite3.connect(DATABASE) as conn:
       
        query = "SELECT id, username, password FROM users WHERE username = ?"
        cursor = conn.execute(query, (username,))
        user = cursor.fetchone()

    if user:
        stored_password_hash = user[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            return {"status": "ok", "user": {"id": user[0], "username": user[1]}}
            
    return {"status": "error", "message": "Invalid credentials"}

def reset_password(user_id: int, new_pass: str) -> bool:
    hashed_password = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt())
    
    with sqlite3.connect(DATABASE) as conn:
        query = "UPDATE users SET password = ? WHERE id = ?"
        conn.execute(query, (hashed_password, user_id))
        conn.commit()
        
    print(f"Password reset for user ID {user_id} completed successfully.")
    return True

def create_user(username: str, password: str, email: str) -> dict:
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    with sqlite3.connect(DATABASE) as conn:
        query = "INSERT INTO users (username, password, email) VALUES (?, ?, ?)"
        conn.execute(query, (username, hashed_password, email))
        conn.commit()
        
    return {"status": "created", "username": username}