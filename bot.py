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
    add_challenge,
    find_challenge,
    assign_challenge,
    save_reply,
    get_completed
)


TOKEN = os.getenv("BOT_TOKEN")


TEXT = {

    "it": {
        "welcome":
        "📸 Benvenuto su PhotoChallenge!\n\n"
        "Invia una foto e qualcuno dovrà ricrearla con una foto dello schermo + mano ✋",

        "challenge":
        "🎯 PHOTO CHALLENGE!\n\n"
        "Ricrea questa foto:\n\n"
        "1️⃣ Aprila su un monitor o telefono\n"
        "2️⃣ Fai una nuova foto\n"
        "3️⃣ La tua mano deve essere visibile ✋",

        "saved":
        "📸 Foto ricevuta!\n"
        "⏳ Sto cercando qualcuno per la challenge...",

        "answer":
        "🔥 Challenge completata!\n\n"
        "Ecco la foto originale e la risposta:"
    },


    "en": {

        "welcome":
        "📸 Welcome to PhotoChallenge!\n\n"
        "Send a photo and someone must recreate it with a screen + hand ✋",

        "challenge":
        "🎯 PHOTO CHALLENGE!\n\n"
        "Recreate this photo:\n\n"
        "1️⃣ Open it on a screen\n"
        "2️⃣ Take a new photo\n"
        "3️⃣ Your hand must be visible ✋",

        "saved":
        "📸 Photo received!\n"
        "⏳ Searching for someone...",

        "answer":
        "🔥 Challenge completed!\n\n"
        "Original photo and reply:"
    }
}



def language(update):

    code = update.effective_user.language_code or "en"

    if code.startswith("it"):
        return "it"

    return "en"




async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    lang = language(update)

    await update.message.reply_text(
        TEXT[lang]["welcome"]
    )




async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_chat.id

    photo = update.message.photo[-1].file_id

    lang = language(update)



    # controllo se è una risposta ad una challenge

    completed = get_completed(user_id)


    if completed is not None:

        save_reply(
            user_id,
            photo
        )

        creator = completed[0]
        original = completed[1]


        await context.bot.send_message(
            user_id,
            "🔥 Foto ricevuta!"
        )


        await context.bot.send_photo(
            creator,
            original,
            caption="📸 Foto originale"
        )


        await context.bot.send_photo(
            creator,
            photo,
            caption="✋ Foto risposta"
        )


        return




    # nuova challenge

    add_challenge(
        user_id,
        photo
    )


    await update.message.reply_text(
        TEXT[lang]["saved"]
    )



    challenge = find_challenge(
        user_id
    )


    if challenge is None:
        return



    challenge_id = challenge[0]

    owner = challenge[1]

    original_photo = challenge[2]



    assign_challenge(
        challenge_id,
        user_id
    )



    await context.bot.send_photo(
        user_id,
        original_photo,
        caption=TEXT[lang]["challenge"]
    )



def create_bot():

    init_db()


    app = Application.builder().token(
        TOKEN
    ).build()



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
