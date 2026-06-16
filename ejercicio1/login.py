import os, sqlite3, hashlib, secrets, logging

logging.basicConfig(level=logging.INFO)
DATABASE = os.getenv("DATABASE", "users.db")

def _hash_password(password: str, salt: bytes = None) -> str:
    salt = salt or secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt.hex() + ":" + dk.hex()

def _verify_password(stored: str, provided: str) -> bool:
    salt_hex, hash_hex = stored.split(":")
    salt = bytes.fromhex(salt_hex)
    dk = hashlib.pbkdf2_hmac("sha256", provided.encode(), salt, 100_000)
    return dk.hex() == hash_hex

def get_user(username: str, password: str) -> dict:
    try:
        with sqlite3.connect(DATABASE) as conn:
            cur = conn.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            if row and _verify_password(row[2], password):
                return {"status": "ok", "user": {"id": row[0], "username": row[1]}}
            return {"status": "error", "message": "Invalid credentials"}
    except Exception as e:
        logging.exception("DB error in get_user")
        return {"status": "error", "message": "Server error"}

def create_user(username: str, password: str, email: str) -> dict:
    pw_hash = _hash_password(password)
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (username, pw_hash, email),
            )
        return {"status": "created", "username": username}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "User exists"}
    except Exception:
        logging.exception("DB error in create_user")
        return {"status": "error", "message": "Server error"}

def reset_password(user_id: int, new_pass: str) -> bool:
    pw_hash = _hash_password(new_pass)
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("UPDATE users SET password = ? WHERE id = ?", (pw_hash, user_id))
        logging.info("Password reset for user %s", user_id)
        return True
    except Exception:
        logging.exception("DB error in reset_password")
        return False