from telegram import Update
from telegram.ext import ContextTypes
from bot.config import ADMIN_IDS
from bot.core import database

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

async def _ensure_admin(update: Update) -> bool:
    user = update.effective_user
    if not is_admin(user.id):
        await update.message.reply_text("❌ আপনি অ্যাডমিন নন।")
        return False
    return True

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await _ensure_admin(update):
        return

    conn = database._conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'")
    pending_withdraws = cur.fetchone()[0]

    conn.close()

    msg = (
        "📊 Stats:\n"
        f"👥 Total users: {total_users}\n"
        f"📝 Total tasks: {total_tasks}\n"
        f"💸 Pending withdraws: {pending_withdraws}\n"
        "🔗 Full control: Web Admin Panel ব্যবহার করুন।"
    )
    await update.message.reply_text(msg)
