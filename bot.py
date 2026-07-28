import os
import asyncio
waiting_photo = None
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://photoroulettebot.onrender.com")
PORT = int(os.getenv("PORT", 10000))

app_web = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()

from telegram.ext import MessageHandler, filters


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
            caption="🎲 La tua foto dalla roulette!"
        )

        await update.message.reply_photo(
            photo=user_photo,
            caption="🎲 La tua foto dalla roulette!"
        )


telegram_app.add_handler(
    MessageHandler(filters.PHOTO, photo_handler)
)

async def start(update: Update, context):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "🎲 Il bot è online!"
    )


telegram_app.add_handler(CommandHandler("start", start))


@app_web.route("/", methods=["GET"])
def home():
    return "PhotoRoulette Bot OK"


@app_web.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    asyncio.create_task(
        telegram_app.process_update(update)
    )

    return "ok"


async def setup():
    await telegram_app.initialize()
    await telegram_app.bot.delete_webhook()
    await telegram_app.bot.set_webhook(
        WEBHOOK_URL + "/webhook"
    )
    print("Webhook impostato:", WEBHOOK_URL + "/webhook")


if __name__ == "__main__":
    asyncio.run(setup())

    app_web.run(
        host="0.0.0.0",
        port=PORT
    )
