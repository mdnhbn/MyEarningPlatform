import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "database.db")

def _conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = _conn()
    cur = conn.cursor()

    # Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            balance REAL DEFAULT 0,
            banned INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tasks
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            reward REAL,
            active INTEGER DEFAULT 1
        )
    """)

    # Required channels
    cur.execute("""
        CREATE TABLE IF NOT EXISTS required_channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE
        )
    """)

    # Withdrawals
    cur.execute("""
        CREATE TABLE IF NOT EXISTS withdrawals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            currency TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Logs
    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            message TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# ---- Shared helpers ----

def get_or_create_user(telegram_id: int):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, telegram_id, balance, banned, created_at FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cur.fetchone()
    if not row:
        cur.execute("INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,))
        conn.commit()
        cur.execute("SELECT id, telegram_id, balance, banned, created_at FROM users WHERE telegram_id = ?", (telegram_id,))
        row = cur.fetchone()
    conn.close()
    return row

def get_balance(telegram_id: int) -> float:
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM users WHERE telegram_id = ?", (telegram_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0.0

def update_balance(telegram_id: int, delta: float):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE telegram_id = ?", (delta, telegram_id))
    conn.commit()
    conn.close()

def log_event(event_type: str, message: str):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (event_type, message) VALUES (?, ?)", (event_type, message))
    conn.commit()
    conn.close()
