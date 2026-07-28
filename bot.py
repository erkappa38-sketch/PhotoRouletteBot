import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 10000))

app_web = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


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
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
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
