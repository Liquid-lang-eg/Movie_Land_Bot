import logging
from aiogram import Dispatcher, Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from .routers import setup_routers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage()) #memory storage - заглушка в итоговом варианте будет подключен redis

setup_routers(dp)

async def start_bot():
    session = AiohttpSession()
    await bot.session.close()
    await dp.start_polling(bot)

