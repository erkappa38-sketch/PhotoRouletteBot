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
    save_reply,
    add_to_gallery,
    get_gallery
)



from collage import create_collage



TOKEN = os.getenv("BOT_TOKEN")





async def start(update, context):

    await update.message.reply_text(
        "📸 Benvenuto su PhotoChallenge!\n\n"
        "Invia una foto per iniziare.\n\n"
        "/gallery per vedere le challenge 🔥"
    )






async def gallery(update, context):


    photos = get_gallery()



    if not photos:

        await update.message.reply_text(
            "📭 Nessuna challenge ancora."
        )

        return



    for photo in photos:


        await context.bot.send_photo(
            update.effective_chat.id,
            photo[0],
            caption="🔥 PhotoChallenge"
        )







async def photo_handler(update, context):


    user_id = update.effective_chat.id


    photo = update.message.photo[-1].file_id




    # controlla se deve rispondere

    active = get_active_challenge(user_id)



    if active:


        challenge_id = active[0]

        creator = active[1]

        original = active[2]



        save_reply(
            challenge_id,
            photo
        )



        collage = await create_collage(
            context.bot,
            original,
            photo
        )



        message = await context.bot.send_photo(
            creator,
            collage,
            caption="🔥 Challenge completata!"
        )



        add_to_gallery(
            message.photo[-1].file_id
        )



        await update.message.reply_text(
            "✅ Risposta inviata!"
        )


        return





    # nuova challenge


    add_challenge(
        user_id,
        photo
    )



    await update.message.reply_text(
        "📸 Foto ricevuta!\n"
        "⏳ Cerco qualcuno..."
    )



    challenge = find_challenge(
        user_id
    )



    if challenge is None:
        return




    assign_challenge(
        challenge[0],
        user_id
    )



    await context.bot.send_photo(
        user_id,
        challenge[2],
        caption=
        "🎯 Ricrea questa foto:\n\n"
        "1️⃣ Aprila su uno schermo\n"
        "2️⃣ Rifai la foto\n"
        "3️⃣ La mano deve essere visibile ✋"
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
        CommandHandler(
            "gallery",
            gallery
        )
    )



    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler
        )
    )


    return app
