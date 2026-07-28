import os

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

waiting_users = []


keyboard = [
    ["🎲 Entra nella roulette"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "Premi il pulsante per entrare nella roulette.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )


async def roulette(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat_id

    if user_id in waiting_users:
        await update.message.reply_text(
            "⏳ Sei già in attesa di un'altra persona."
        )
        return

    waiting_users.append(user_id)

    if len(waiting_users) >= 2:
        user1 = waiting_users.pop(0)
        user2 = waiting_users.pop(0)

        # sicurezza: mai abbinare la stessa persona
        if user1 == user2:
            waiting_users.insert(0, user1)
            return

        await context.bot.send_message(
            user1,
            "🎲 Sei stato abbinato! Ora invia una foto."
        )

        await context.bot.send_message(
            user2,
            "🎲 Sei stato abbinato! Ora invia una foto."
        )

    else:
        await update.message.reply_text(
            "⏳ Sei in attesa di un'altra persona..."
        )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Foto ricevuta! La roulette è pronta."
    )


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.Regex("🎲 Entra nella roulette"),
            roulette
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )

    print("Bot avviato...")

    app.run_polling()


if __name__ == "__main__":
    main()
