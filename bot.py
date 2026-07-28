import os

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
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
        "welcome":
            "📸 Benvenuto su PhotoRoulette!\n\n"
            "Invia una foto e verrà abbinata casualmente "
            "con un'altra persona 🎲",

        "received":
            "📸 Foto ricevuta!\n"
            "🎲 Cerco un abbinamento...",

        "match":
            "🎲 Ecco la foto del tuo abbinamento!"
    },

    "en": {
        "welcome":
            "📸 Welcome to PhotoRoulette!\n\n"
            "Send a photo and it will be randomly matched "
            "with another person 🎲",

        "received":
            "📸 Photo received!\n"
            "🎲 Looking for a match...",

        "match":
            "🎲 Here's your roulette match!"
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

    user_id = update.message.chat_id

    photo = update.message.photo[-1].file_id

    lang = get_lang(update)


    # salva la foto nel database
    add_photo(
        user_id,
        photo,
        lang
    )


    await update.message.reply_text(
        TEXT[lang]["received"]
    )


    # cerca qualcuno da abbinare
    match = get_match(user_id)


    if not match:
        return


    photo_id = match[0]
    other_user = match[1]
    other_photo = match[2]
    other_lang = match[3]


    # manda le foto scambiate

    await context.bot.send_photo(
        chat_id=user_id,
        photo=other_photo,
        caption=TEXT[lang]["match"]
    )


    await context.bot.send_photo(
        chat_id=other_user,
        photo=photo,
        caption=TEXT[other_lang]["match"]
    )


    # elimina entrambe dalla coda

    delete_photo(photo_id)



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
