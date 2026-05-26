import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import router

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()


async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set in the environment variables.")
    bot = Bot(token=TOKEN)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
