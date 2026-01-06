import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "database.db")

def _conn():
    return sqlite3.connect(DB_PATH)

def get_stats():
    conn = _conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'")
    pending_withdraws = cur.fetchone()[0]

    conn.close()
    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "pending_withdraws": pending_withdraws,
    }

# ---- Tasks ----
def list_tasks():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, link, reward, active FROM tasks ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_task(title, link, reward):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, link, reward, active) VALUES (?, ?, ?, 1)",
        (title, link, reward),
    )
    conn.commit()
    conn.close()

def remove_task(task_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def set_task_active(task_id, active: bool):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET active = ? WHERE id = ?",
        (1 if active else 0, task_id),
    )
    conn.commit()
    conn.close()

# ---- Channels ----
def list_channels():
    conn = _conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username FROM required_channels ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_channel(username):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO required_channels (username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def remove_channel(channel_id):
    conn = _conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM required_channels WHERE id = ?", (channel_id,))
    conn.commit()
    conn.close()

# ---- Users ----
def list_users(limit=50):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, telegram_id, balance, banned FROM users ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def set_user_ban(user_id, banned: bool):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET banned = ? WHERE id = ?",
        (1 if banned else 0, user_id),
    )
    conn.commit()
    conn.close()

# ---- Withdraws ----
def list_withdraws(status="pending"):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, amount, currency, status, created_at "
        "FROM withdrawals WHERE status = ? ORDER BY id DESC",
        (status,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def update_withdraw(withdraw_id, status):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE withdrawals SET status = ? WHERE id = ?",
        (status, withdraw_id),
    )
    conn.commit()
    conn.close()

# ---- Logs ----
def list_logs(limit=100):
    conn = _conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, event_type, message, created_at "
        "FROM logs ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
