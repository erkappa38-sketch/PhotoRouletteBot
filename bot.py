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
# formato:
# [
#   {"id": utente, "photo": foto}
# ]
photo_queue = []


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "Invia una o più foto.\n"
        "Ogni foto verrà abbinata casualmente con la foto di un'altra persona 🎲"
    )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id
    photo_id = update.message.photo[-1].file_id


    # salva ogni singola foto
    photo_queue.append(
        {
            "id": user_id,
            "photo": photo_id
        }
    )


    await update.message.reply_text(
        "📸 Foto ricevuta!\n"
        "🎲 Cerco un abbinamento..."
    )


    # servono almeno due foto
    if len(photo_queue) < 2:
        return


    # mescola per rendere casuale
    random.shuffle(photo_queue)


    trovato = False


    for i in range(len(photo_queue)):

        for j in range(i + 1, len(photo_queue)):


            # controlla che siano due persone diverse
            if photo_queue[i]["id"] != photo_queue[j]["id"]:


                foto1 = photo_queue.pop(j)
                foto2 = photo_queue.pop(i)


                # manda la foto dell'altro
                await context.bot.send_photo(
                    chat_id=foto1["id"],
                    photo=foto2["photo"],
                    caption="🎲 La tua foto dalla roulette!"
                )


                await context.bot.send_photo(
                    chat_id=foto2["id"],
                    photo=foto1["photo"],
                    caption="🎲 La tua foto dalla roulette!"
                )


                trovato = True
                break


        if trovato:
            break



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
