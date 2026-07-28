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
    get_active_challenge,
    save_reply
)


from collage import create_collage



TOKEN = os.getenv("BOT_TOKEN")



TEXT = {

    "it": {

        "welcome":
        "📸 Benvenuto su PhotoChallenge!\n\n"
        "Invia una foto e qualcuno dovrà ricrearla con schermo + mano ✋",


        "waiting":
        "📸 Foto ricevuta!\n"
        "⏳ Sto cercando qualcuno...",


        "challenge":
        "🎯 PHOTO CHALLENGE\n\n"
        "Ricrea questa foto:\n\n"
        "1️⃣ Aprila su un monitor o telefono\n"
        "2️⃣ Fai una nuova foto\n"
        "3️⃣ La tua mano deve essere visibile ✋",


        "done":
        "🔥 Challenge completata!"

    },


    "en": {

        "welcome":
        "📸 Welcome to PhotoChallenge!\n\n"
        "Send a photo and someone will recreate it with screen + hand ✋",


        "waiting":
        "📸 Photo received!\n"
        "⏳ Searching someone...",


        "challenge":
        "🎯 PHOTO CHALLENGE\n\n"
        "Recreate this photo:\n\n"
        "1️⃣ Open it on a screen\n"
        "2️⃣ Take a new photo\n"
        "3️⃣ Your hand must be visible ✋",


        "done":
        "🔥 Challenge completed!"

    }

}




def get_lang(update):

    lang = update.effective_user.language_code or "en"

    if lang.startswith("it"):
        return "it"

    return "en"






async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    lang = get_lang(update)


    await update.message.reply_text(
        TEXT[lang]["welcome"]
    )







async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):


    user_id = update.effective_chat.id

    photo = update.message.photo[-1].file_id

    lang = get_lang(update)



    # controlla se l'utente deve rispondere

    active = get_active_challenge(
        user_id
    )



    if active:


        challenge_id = active[0]

        creator = active[1]

        original = active[2]



        # salva risposta

        save_reply(
            challenge_id,
            photo
        )



        # crea collage

        collage = await create_collage(
            context.bot,
            original,
            photo
        )



        # manda solo il collage al creatore

        await context.bot.send_photo(
            chat_id=creator,
            photo=collage,
            caption=
            "🔥 Photo Challenge completata!\n\n"
            "📸 Originale + ✋ Risposta"
        )



        await update.message.reply_text(
            TEXT[lang]["done"]
        )


        return






    # nuova sfida

    add_challenge(
        user_id,
        photo
    )



    await update.message.reply_text(
        TEXT[lang]["waiting"]
    )



    challenge = find_challenge(
        user_id
    )



    if challenge is None:

        return




    challenge_id = challenge[0]

    original_photo = challenge[2]



    assign_challenge(
        challenge_id,
        user_id
    )



    await context.bot.send_photo(
        chat_id=user_id,
        photo=original_photo,
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
