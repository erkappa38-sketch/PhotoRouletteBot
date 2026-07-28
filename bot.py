import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))

app_web = Flask(__name__)

telegram_app = Application.builder().token(TOKEN).build()


async def start(update, context):
    await update.message.reply_text(
        "📸 Benvenuto su PhotoRoulette!\n\n"
        "🎲 Roulette fotografica anonima in arrivo!"
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


if __name__ == "__main__":
    import asyncio

    asyncio.run(telegram_app.initialize())

    webhook_url = os.getenv("WEBHOOK_URL")
    asyncio.run(
        telegram_app.bot.set_webhook(
            webhook_url + "/webhook"
        )
    )

    app_web.run(
        host="0.0.0.0",
        port=PORT
    )
