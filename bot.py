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


# coda delle foto in attesa
photo_queue = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "Invia una foto e verrai abbinato casualmente con un'altra persona 🎲"
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id
    photo_id = update.message.photo[-1].file_id


    # evita doppioni in coda
    for user in photo_queue:
        if user["id"] == user_id:
            await update.message.reply_text(
                "⏳ Hai già una foto in attesa..."
            )
            return


  


    await update.message.reply_text(
        "📸 Foto ricevuta!\n"
        "🎲 Sto cercando un abbinamento..."
    )


    # servono almeno due persone
    if len(photo_queue) < 2:
        return


    # mescola la coda
    random.shuffle(photo_queue)


    user1 = photo_queue.pop(0)
    user2 = photo_queue.pop(0)


    # invia foto scambiate

    await context.bot.send_photo(
        chat_id=user1["id"],
        photo=user2["photo"],
        caption="🎲 La tua foto dalla roulette!"
    )


    await context.bot.send_photo(
        chat_id=user2["id"],
        photo=user1["photo"],
        caption="🎲 La tua foto dalla roulette!"
    )



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
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
