import os
import asyncio
import threading

from flask import Flask, request
from telegram import Update

from bot import create_bot


PORT = int(os.getenv("PORT", 10000))

RENDER_URL = os.getenv(
    "RENDER_EXTERNAL_URL",
    "https://photoroulettebot.onrender.com"
)


app_web = Flask(__name__)


telegram_app = create_bot()


# unico event loop sempre aperto
loop = asyncio.new_event_loop()


def run_loop():

    asyncio.set_event_loop(loop)

    loop.run_forever()



threading.Thread(
    target=run_loop,
    daemon=True
).start()



@app_web.route("/", methods=["GET"])
def home():

    return "PhotoRoulette Bot Online"



@app_web.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json(force=True)


    update = Update.de_json(
        data,
        telegram_app.bot
    )


    asyncio.run_coroutine_threadsafe(
        telegram_app.process_update(update),
        loop
    )


    return "ok"



async def setup():

    await telegram_app.initialize()

    await telegram_app.start()


    webhook_url = (
        RENDER_URL +
        "/webhook"
    )


    await telegram_app.bot.delete_webhook()


    await telegram_app.bot.set_webhook(
        webhook_url
    )


    print(
        "Webhook attivo:",
        webhook_url
    )



asyncio.run_coroutine_threadsafe(
    setup(),
    loop
)



app_web.run(
    host="0.0.0.0",
    port=PORT
)
