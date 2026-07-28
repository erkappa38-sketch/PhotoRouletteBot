import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "🎲 Cerca una persona casuale e scambia immagini in modo anonimo."
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()
