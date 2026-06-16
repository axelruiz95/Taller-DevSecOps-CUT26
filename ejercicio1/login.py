import sqlite3
import hashlib
import hmac
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE = os.environ.get("DATABASE", "users.db")


def _hash_password(password: str) -> str:
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + ":" + key.hex()


def _verify_password(password: str, stored_hash: str) -> bool:
    salt_hex, key_hex = stored_hash.split(":")
    salt = bytes.fromhex(salt_hex)
    key = bytes.fromhex(key_hex)
    new_key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return hmac.compare_digest(new_key, key)


def get_user(username: str, password: str) -> dict:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        user = cursor.fetchone()

    if user and _verify_password(password, user[2]):
        return {"status": "ok", "user": {"id": user[0], "username": user[1]}}
    return {"status": "error", "message": "Invalid credentials"}


def reset_password(user_id: int, new_pass: str) -> bool:
    hashed = _hash_password(new_pass)
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "UPDATE users SET password = ? WHERE id = ?", (hashed, user_id)
        )
    return True


def create_user(username: str, password: str, email: str) -> dict:
    hashed = _hash_password(password)
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed, email),
        )
    return {"status": "created", "username": username}