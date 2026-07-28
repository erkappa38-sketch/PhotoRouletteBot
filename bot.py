import os
import random

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

# Coda delle foto
photo_queue = []

# Testi
TEXT = {
    "it": {
        "welcome":
            "📸 Benvenuto su PhotoRoulette!\n\n"
            "Invia una o più foto.\n"
            "Ogni foto verrà abbinata casualmente con un'altra persona 🎲",

        "received":
            "📸 Foto ricevuta!\n"
            "🎲 Sto cercando un abbinamento...",

        "matched":
            "🎲 Ecco la foto del tuo abbinamento!"
    },

    "en": {
        "welcome":
            "📸 Welcome to PhotoRoulette!\n\n"
            "Send one or more photos.\n"
            "Each photo will be randomly matched with another person 🎲",

        "received":
            "📸 Photo received!\n"
            "🎲 Looking for a match...",

        "matched":
            "🎲 Here's your match!"
    }
}


def get_lang(update):
    lang = update.effective_user.language_code or "en"

    if lang.lower().startswith("it"):
        return "it"

    return "en"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lang = get_lang(update)

    await update.message.reply_text(
        TEXT[lang]["welcome"]
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id
    photo = update.message.photo[-1].file_id
    lang = get_lang(update)

    # salva SEMPRE ogni foto
    photo_queue.append({
        "id": user_id,
        "photo": photo,
        "lang": lang
    })

    await update.message.reply_text(
        TEXT[lang]["received"]
    )

    if len(photo_queue) < 2:
        return

    random.shuffle(photo_queue)

    for i in range(len(photo_queue)):

        for j in range(i + 1, len(photo_queue)):

            if photo_queue[i]["id"] != photo_queue[j]["id"]:

                first = photo_queue.pop(j)
                second = photo_queue.pop(i)

                await context.bot.send_photo(
                    chat_id=first["id"],
                    photo=second["photo"],
                    caption=TEXT[first["lang"]]["matched"]
                )

                await context.bot.send_photo(
                    chat_id=second["id"],
                    photo=first["photo"],
                    caption=TEXT[second["lang"]]["matched"]
                )

                return


def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
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
