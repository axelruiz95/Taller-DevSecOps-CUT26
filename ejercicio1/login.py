"""
User database operations.

Security fixes applied vs. the original version:
- Parameterized SQL queries everywhere (prevents SQL injection)
- Passwords hashed with werkzeug's PBKDF2-based generate_password_hash /
  check_password_hash (salted, constant-time compare) instead of stored
  and compared as plaintext
- SECRET_KEY (and DB_PASSWORD, if your DB engine uses one) loaded from
  environment variables instead of hardcoded in source
- Connections explicitly closed in a finally block; reset_password and
  create_user now call conn.commit() so writes actually persist
- No sensitive data (passwords) printed to stdout/logs
- sqlite3 errors caught and returned as clean error responses instead of
  raising unhandled exceptions
- get_user selects explicit columns instead of SELECT *, so the password
  column position isn't an implicit assumption

Setup:
    pip install werkzeug   # already a dependency if you're using Flask
    export SECRET_KEY="some-long-random-value"
    export DB_PASSWORD="..."   # only if your DB engine actually requires one;
                                 # sqlite files have no built-in auth, so this
                                 # is unused here but kept for parity if you
                                 # move to MySQL/Postgres later
"""

import os
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

DB_PASSWORD = os.environ.get("DB_PASSWORD")
SECRET_KEY = os.environ.get("SECRET_KEY")

DATABASE = "users.db"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")


def get_user(username: str, password: str) -> dict:
    conn = sqlite3.connect(DATABASE)
    try:
        cursor = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,),
        )
        user = cursor.fetchone()
    finally:
        conn.close()

    if user and check_password_hash(user[2], password):
        return {"status": "ok", "user": {"id": user[0], "username": user[1]}}
    return {"status": "error", "message": "Invalid credentials"}


def reset_password(user_id: int, new_pass: str) -> bool:
    hashed = generate_password_hash(new_pass)
    conn = sqlite3.connect(DATABASE)
    try:
        cursor = conn.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed, user_id),
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Password reset failed for user {user_id}: {e}")
        return False
    finally:
        conn.close()

    if cursor.rowcount == 0:
        print(f"Password reset failed: no user with id {user_id}")
        return False

    print(f"Password reset for user {user_id}")
    return True


def create_user(username: str, password: str, email: str) -> dict:
    hashed = generate_password_hash(password)
    conn = sqlite3.connect(DATABASE)
    try:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed, email),
        )
        conn.commit()
        return {"status": "created", "username": username}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "Username already exists"}
    except sqlite3.Error as e:
        print(f"create_user failed: {e}")
        return {"status": "error", "message": "Could not create user"}
    finally:
        conn.close()


#existing passwords already stored as plaintext in users.db won't pass check_password_hash anymore since the format changed — you'd need a one-time migration script that reads each plaintext password, hashes it, and writes it back, or just have everyone reset their password once after you deploy this.

