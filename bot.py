import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

waiting_photo = None


async def start(update: Update, context):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "🎲 Invia una foto e cercherò un'altra persona."
    )


async def photo_handler(update: Update, context):
    global waiting_photo

    user_photo = update.message.photo[-1].file_id

    if waiting_photo is None:
        waiting_photo = user_photo
        await update.message.reply_text(
            "📸 Foto ricevuta!\nSto cercando un'altra persona..."
        )

    else:
        other_photo = waiting_photo
        waiting_photo = None

        await update.message.reply_photo(
            photo=other_photo,
            caption="🎲 Foto dalla roulette!"
        )

        await update.message.reply_photo(
            photo=user_photo,
            caption="🎲 Foto dalla roulette!"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.PHOTO, photo_handler)
    )

    print("Bot avviato...")

    app.run_polling()


if __name__ == "__main__":
    main()
