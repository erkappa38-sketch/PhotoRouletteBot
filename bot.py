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
matched_users = {}
photos = {}


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
            "⏳ Sei già in attesa."
        )
        return

    waiting_users.append(user_id)

    if len(waiting_users) >= 2:

        user1 = waiting_users.pop(0)
        user2 = waiting_users.pop(0)

        if user1 == user2:
            return

        matched_users[user1] = user2
        matched_users[user2] = user1

        await context.bot.send_message(
            user1,
            "🎲 Sei stato abbinato! Ora manda una foto 📸"
        )

        await context.bot.send_message(
            user2,
            "🎲 Sei stato abbinato! Ora manda una foto 📸"
        )

    else:
        await update.message.reply_text(
            "⏳ Sei in attesa di un'altra persona..."
        )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id
    photo = update.message.photo[-1].file_id

    photos[user_id] = photo

    if user_id not in matched_users:
        await update.message.reply_text(
            "📸 Foto ricevuta! Prima entra nella roulette 🎲"
        )
        return

    other_user = matched_users[user_id]

    if other_user in photos:

        await context.bot.send_photo(
            chat_id=user_id,
            photo=photos[other_user],
            caption="🎲 Ecco la foto del tuo abbinamento!"
        )

        await context.bot.send_photo(
            chat_id=other_user,
            photo=photos[user_id],
            caption="🎲 Ecco la foto del tuo abbinamento!"
        )

        del photos[user_id]
        del photos[other_user]

    else:
        await update.message.reply_text(
            "📸 Foto salvata! Aspetto l'altra persona..."
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
