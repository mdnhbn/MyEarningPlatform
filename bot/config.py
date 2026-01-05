import os

# Telegram bot token (Railway env var থেকে নেবে)
TOKEN = os.getenv("TOKEN", "7779213791:AAFnhlnkFIwNTiswoqxQkgTdl0DGSfZhemI")

# Admin Telegram IDs (comma separated)
ADMIN_IDS = [
    int(x) for x in os.getenv("ADMIN_IDS", "929198867").split(",") if x.strip()
]

# SQLite DB path (bot + backend দুই জায়গায় একই DB ব্যবহার করবে)
DB_PATH = os.getenv("DB_PATH", "database.db")
