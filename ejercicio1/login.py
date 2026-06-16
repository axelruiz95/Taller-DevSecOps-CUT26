import sqlite3
import hashlib

DATABASE = "users.db"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_user(username: str, password: str) -> dict:
    try:
        with sqlite3.connect(DATABASE) as conn:

            cursor = conn.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,)
            )

            user = cursor.fetchone()

            if user and user[2] == hash_password(password):
                return {
                    "status": "ok",
                    "user": {
                        "id": user[0],
                        "username": user[1]
                    }
                }

            return {
                "status": "error",
                "message": "Invalid credentials"
            }

    except sqlite3.Error:
        return {
            "status": "error",
            "message": "Database error"
        }


def create_user(username: str, password: str, email: str) -> dict:
    try:
        hashed_password = hash_password(password)

        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                """
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
                """,
                (username, hashed_password, email)
            )

            conn.commit()

        return {
            "status": "created",
            "username": username
        }

    except sqlite3.Error:
        return {
            "status": "error",
            "message": "User could not be created"
        }


def reset_password(user_id: int, new_pass: str) -> bool:
    try:
        hashed_password = hash_password(new_pass)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.execute(
                """
                UPDATE users
                SET password = ?
                WHERE id = ?
                """,
                (hashed_password, user_id)
            )

            conn.commit()

            return cursor.rowcount > 0

    except sqlite3.Error:
        return False