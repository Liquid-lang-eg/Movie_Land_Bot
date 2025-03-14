from aiogram import Router, F
from aiogram.types import Message
from app.bot.keyboards.inline import main_menu  # Импортируем клавиатуру
from config import BACKEND_URL
from aiohttp import ClientSession

router = Router()

@router.message(F.text == "/start")
async def start_cmd(message: Message):
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/auth/register", json={
            "id": message.from_user.id,
            "username": message.from_user.username or f"user_{message.from_user.id}"
        }) as resp:
            await message.answer("👋 Добро пожаловать! Выберите действие:", reply_markup=main_menu())

