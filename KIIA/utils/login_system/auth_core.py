import sqlite3
import time
import secrets
import os
from utils.tools.logger import print

path = os.path.expandvars("C:/Users/%USERNAME%/OneDrive/Desktop/KIIA/KIIA_OUTPUT")
os.makedirs(path, exist_ok=True)
path_log = os.path.join(path, "user_credentials.db")

KEYZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
DB_PATH = path_log
SESSION_DAYS = 366 * 24 * 60 * 60

def generate_token(length=128):
    return "".join(secrets.choice(KEYZ) for _ in range(length))

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            created_at INTEGER,
            expires_at INTEGER
        )
    """)
    conn.commit()
    conn.close()

def create_session():
    token = generate_token()
    now = int(time.time())
    expires = now + SESSION_DAYS

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO sessions VALUES (?, ?, ?)",
        (token, now, expires)
    )
    conn.commit()
    conn.close()

    return token

def validate_token(token):
    now = int(time.time())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT expires_at FROM sessions WHERE token = ?",
        (token,)
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    return now < row[0]


def pre_check():
    try:
        now = int(time.time())

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 1
            FROM sessions
            WHERE expires_at IS NULL
               OR expires_at > ?
            LIMIT 1
        """, (now,))

        return cursor.fetchone() is not None

    except sqlite3.Error as e:
        print(f"Security DB error: {e}")
        return False

    finally:
        if 'conn' in locals():
            conn.close()

def cleanup_expired():
    now = int(time.time())

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "DELETE FROM sessions WHERE expires_at < ?",
        (now,)
    )
    conn.commit()
    conn.close()
