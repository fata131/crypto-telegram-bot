import sqlite3
from datetime import datetime, timedelta

# Create database (auto)
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    plan TEXT DEFAULT 'free',
    expires_at TEXT
)
""")
conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()


def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()


def is_premium(user_id, owner_id):
    # Owner is always premium
    if user_id == owner_id:
        return True

    user = get_user(user_id)
    if not user:
        return False

    plan = user[1]
    expires_at = user[2]

    if plan != "premium" or not expires_at:
        return False

    return datetime.utcnow() < datetime.fromisoformat(expires_at)


def upgrade_user(user_id, days):
    expiry = datetime.utcnow() + timedelta(days=days)
    cursor.execute(
        "UPDATE users SET plan='premium', expires_at=? WHERE user_id=?",
        (expiry.isoformat(), user_id)
    )
    conn.commit()
