import sqlite3
from datetime import datetime

# =========================
# DATABASE CONNECTION
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# USERS TABLE
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# MESSAGES TABLE (CHAT HISTORY)
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================
# USER MANAGEMENT
# =========================
def get_or_create_user(user_id: str):
    cursor.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user:
        cursor.execute(
            "INSERT INTO users (user_id, created_at) VALUES (?, ?)",
            (user_id, datetime.now())
        )
        conn.commit()

    return user_id


# =========================
# SAVE MESSAGE (CHAT HISTORY)
# =========================
def save_message(user_id: str, role: str, message: str):
    try:
        cursor.execute("""
            INSERT INTO messages (user_id, role, message)
            VALUES (?, ?, ?)
        """, (user_id, role, message))

        conn.commit()

    except Exception as e:
        print("❌ DB Save Error:", e)


# =========================
# GET CHAT HISTORY
# =========================
def get_messages(user_id: str, limit: int = 20):
    try:
        cursor.execute("""
            SELECT role, message
            FROM messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()

        # reverse to show correct order (old → new)
        return [
            {"role": r[0], "content": r[1]}
            for r in reversed(rows)
        ]

    except Exception as e:
        print("❌ DB Fetch Error:", e)
        return []
