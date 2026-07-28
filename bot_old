import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")

waiting_photo = None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "Invia una foto e il bot la scambierà "
        "con quella di un altro utente."
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_photo

    photo = update.message.photo[-1].file_id

    if waiting_photo is None:
        waiting_photo = photo

        await update.message.reply_text(
            "🎲 Foto ricevuta!\n"
            "Sto cercando un'altra persona..."
        )

    else:
        other_photo = waiting_photo
        waiting_photo = None

        await update.message.reply_photo(
            photo=other_photo,
            caption="🎲 Ecco la foto dell'altra persona!"
        )

        await update.message.reply_photo(
            photo=photo,
            caption="🎲 Ecco la foto dell'altra persona!"
        )


def main():

    if not TOKEN:
        print("ERRORE: manca BOT_TOKEN")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(filters.PHOTO, photo_handler)
    )

    print("Bot avviato...")

    app.run_polling()


if __name__ == "__main__":
    main()
