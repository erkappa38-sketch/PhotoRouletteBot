import os
import asyncio
from bot import app_web, setup

if __name__ == "__main__":
    asyncio.run(setup())

    port = int(os.environ.get("PORT", 10000))

    app_web.run(
        host="0.0.0.0",
        port=port
    )
