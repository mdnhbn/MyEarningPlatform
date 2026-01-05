from telegram import Update
from telegram.ext import ContextTypes
from bot.core import database

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    database.get_or_create_user(user.id)
    await update.message.reply_text(
        "👋 স্বাগতম MyEarningPlatform এ!\n\n"
        "👉 রেজিস্টার: /register\n"
        "👉 কাজ দেখুন: /tasks\n"
        "👉 ব্যালেন্স: /balance\n"
        "👉 উইথড্র: /withdraw\n"
    )

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    database.get_or_create_user(user.id)
    await update.message.reply_text("✅ আপনি সফলভাবে রেজিস্টার করেছেন!")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bal = database.get_balance(user.id)
    await update.message.reply_text(f"💰 আপনার ব্যালেন্স: {bal}")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = database._conn()
    cur = conn.cursor()
    cur.execute("SELECT id, title, link, reward, active FROM tasks WHERE active = 1 ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("📝 কোনো টাস্ক নেই এখন।")
        return

    text_lines = ["📝 উপলব্ধ টাস্কসমূহ:\n"]
    for t in rows:
        text_lines.append(f"#{t[0]} — {t[1]} ({t[3]} পয়েন্ট)\n{t[2]}\n")

    await update.message.reply_text("\n".join(text_lines))

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    if not args:
        await update.message.reply_text("কোন টাস্ক শেষ করেছেন? `/done 1` এইভাবে পাঠান।")
        return

    try:
        task_id = int(args[0])
    except ValueError:
        await update.message.reply_text("সঠিক টাস্ক আইডি দিন। উদাহরণ: `/done 1`")
        return

    conn = database._conn()
    cur = conn.cursor()
    cur.execute("SELECT reward FROM tasks WHERE id = ? AND active = 1", (task_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        await update.message.reply_text("❌ টাস্ক পাওয়া যায়নি বা ইনএক্টিভ।")
        return

    reward = row[0]
    database.update_balance(user.id, reward)
    database.log_event("task_done", f"user {user.id} completed task {task_id} and got {reward}")
    await update.message.reply_text(f"✅ টাস্ক #{task_id} সম্পন্ন! {reward} পয়েন্ট যোগ হয়েছে।")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args

    if len(args) < 2:
        await update.message.reply_text("উদাহরণ: `/withdraw 10 USD`")
        return

    try:
        amount = float(args[0])
    except ValueError:
        await update.message.reply_text("সঠিক অ্যামাউন্ট দিন। উদাহরণ: `/withdraw 10 USD`")
        return

    currency = args[1].upper()
    balance = database.get_balance(user.id)
    if amount > balance:
        await update.message.reply_text("❌ আপনার ব্যালেন্সে এত টাকা নেই।")
        return

    conn = database._conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE telegram_id = ?", (user.id,))
    row = cur.fetchone()
    if not row:
        await update.message.reply_text("❌ ইউজার পাওয়া যায়নি। আগে /register দিন।")
        conn.close()
        return

    user_id = row[0]
    cur.execute(
        "INSERT INTO withdrawals (user_id, amount, currency, status) VALUES (?, ?, ?, 'pending')",
        (user_id, amount, currency),
    )
    conn.commit()
    conn.close()

    database.update_balance(user.id, -amount)
    database.log_event("withdraw_request", f"user {user.id} requested {amount} {currency}")
    await update.message.reply_text("✅ আপনার উইথড্র রিকোয়েস্ট রিসিভ করা হয়েছে। অ্যাডমিন রিভিউ করবে।")
