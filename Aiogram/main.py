import asyncio
import logging
from aiogram import Bot, Dispatcher
# from app.database import create_tables
# from app.bot.handlers import setup_dispatcher
from app.config import TELEGRAM_TOKEN
from app.bot.handlers import rt
from aiogram.fsm.strategy import FSMStrategy
import os
import sys
from app.core import *
from sqlalchemy.orm import Session


async def main():

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token="7168083726:AAHYLIR0MO41KpFu-NSI1D0iaNn6l6UVAkw")
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

    dp.include_router(router=rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    create_tables()
    asyncio.run(main())
