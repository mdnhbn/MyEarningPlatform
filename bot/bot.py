from telegram.ext import Application, CommandHandler
from bot.config import TOKEN
from bot.core import database
from bot.panels import user_panel, admin_panel

def main():
    database.init_db()
    app = Application.builder().token(TOKEN).build()

    # User commands
    app.add_handler(CommandHandler("start", user_panel.start))
    app.add_handler(CommandHandler("register", user_panel.register))
    app.add_handler(CommandHandler("balance", user_panel.balance))
    app.add_handler(CommandHandler("tasks", user_panel.tasks))
    app.add_handler(CommandHandler("done", user_panel.done))
    app.add_handler(CommandHandler("withdraw", user_panel.withdraw))

    # Admin commands
    app.add_handler(CommandHandler("stats", admin_panel.stats))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
