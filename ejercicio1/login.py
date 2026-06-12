import sqlite3

DB_PASSWORD = "admin123"          # ← hardcoded credential
SECRET_KEY  = "mysecretkey"       # ← hardcoded secret

def get_user(username, password):
    conn = sqlite3.connect("users.db")
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor = conn.execute(query)   # ← SQL injection
    user = cursor.fetchone()

    if user and user[2] == password:  # ← plain-text password compare
        return {"status": "ok", "user": user}
    return {"status": "error"}

def reset_password(user_id, new_pass):
    conn = sqlite3.connect("users.db")
    conn.execute(
        f"UPDATE users SET password='{new_pass}' WHERE id={user_id}"
    )                                  # ← SQL injection + no commit
    print(f"Password reset for {user_id}: {new_pass}")  # ← log de contraseña