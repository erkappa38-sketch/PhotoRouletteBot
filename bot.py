import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from database import (
    init_db,
    add_photo,
    get_match,
    delete_photo
)


TOKEN = os.getenv("BOT_TOKEN")


TEXT = {
    "it": {
        "welcome": "📸 Benvenuto su PhotoRoulette!\n\nInvia una foto e cercherò un abbinamento casuale 🎲",
        "waiting": "📸 Foto ricevuta!\n⏳ Aspetto un'altra persona...",
        "match": "🎲 Ecco la foto del tuo abbinamento!"
    },
    "en": {
        "welcome": "📸 Welcome to PhotoRoulette!\n\nSend a photo and I will find a random match 🎲",
        "waiting": "📸 Photo received!\n⏳ Waiting for another person...",
        "match": "🎲 Here's your match!"
    }
}


def get_lang(update):
    lang = update.effective_user.language_code or "en"

    if lang.startswith("it"):
        return "it"

    return "en"



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    lang = get_lang(update)

    await update.message.reply_text(
        TEXT[lang]["welcome"]
    )



async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_chat.id

    photo_id = update.message.photo[-1].file_id

    lang = get_lang(update)


    # prima salvo la foto
    add_photo(
        user_id,
        photo_id,
        lang
    )


    # cerco un'altra persona
    match = get_match(user_id)


    if match is None:

        await update.message.reply_text(
            TEXT[lang]["waiting"]
        )

        return



    database_id = match[0]
    other_user = match[1]
    other_photo = match[2]
    other_lang = match[3]


    # invio scambio

    await context.bot.send_photo(
        chat_id=user_id,
        photo=other_photo,
        caption=TEXT[lang]["match"]
    )


    await context.bot.send_photo(
        chat_id=other_user,
        photo=photo_id,
        caption=TEXT[other_lang]["match"]
    )


    # elimino la foto dell'altro utente
    delete_photo(database_id)



def create_bot():

    init_db()

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


    return app
