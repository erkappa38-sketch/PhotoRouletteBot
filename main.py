import os
import asyncio

from flask import Flask, request

from telegram import Update

from bot import create_bot


PORT = int(os.getenv("PORT", 10000))

RENDER_URL = os.getenv(
    "RENDER_EXTERNAL_URL"
)


app_web = Flask(__name__)


telegram_app = create_bot()



@app_web.route("/", methods=["GET"])
def home():

    return "PhotoRoulette Bot Online"



@app_web.route("/webhook", methods=["POST"])
async def webhook():

    data = request.get_json(force=True)

    update = Update.de_json(
        data,
        telegram_app.bot
    )


    await telegram_app.process_update(
        update
    )


    return "ok"



async def setup():

    await telegram_app.initialize()


    webhook_url = (
        RENDER_URL
        + "/webhook"
    )


    await telegram_app.bot.delete_webhook()


    await telegram_app.bot.set_webhook(
        webhook_url
    )


    print(
        "Webhook attivo:",
        webhook_url
    )



if __name__ == "__main__":


    asyncio.run(
        setup()
    )


    app_web.run(
        host="0.0.0.0",
        port=PORT
    )
