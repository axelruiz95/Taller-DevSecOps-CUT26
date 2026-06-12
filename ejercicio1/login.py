import sqlite3

DB_PASSWORD = "admin123"
SECRET_KEY = "mysecretkey"

DATABASE = "users.db"


def get_user(username: str, password: str) -> dict:
    conn = sqlite3.connect(DATABASE)
    query = f"SELECT * FROM users WHERE username='{username}'"
    cursor = conn.execute(query)
    user = cursor.fetchone()

    if user and user[2] == password:
        return {"status": "ok", "user": {"id": user[0], "username": user[1]}}
    return {"status": "error", "message": "Invalid credentials"}


def reset_password(user_id: int, new_pass: str) -> bool:
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        f"UPDATE users SET password='{new_pass}' WHERE id={user_id}"
    )
    print(f"Password reset for user {user_id}: {new_pass}")
    return True


def create_user(username: str, password: str, email: str) -> dict:
    conn = sqlite3.connect(DATABASE)
    conn.execute(
        f"INSERT INTO users (username, password, email) "
        f"VALUES ('{username}', '{password}', '{email}')"
    )
    conn.commit()
    conn.close()
    return {"status": "created", "username": username}
