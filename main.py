from bot import app_web

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 10000))

    app_web.run(
        host="0.0.0.0",
        port=port
    )
