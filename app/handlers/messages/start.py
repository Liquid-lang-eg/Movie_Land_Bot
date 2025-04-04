from aiogram import Router, F
from aiogram.types import Message
from keyboards.inline import main_menu
from backend_requests import register_user_in_backend

router = Router()


@router.message(F.text == "/start")
async def start_cmd(message: Message):
    # Регистрируем пользователя через бэкенд
    backend_response = await register_user_in_backend(message.from_user.id)

    await message.answer(
        "👋 Добро пожаловать! Выберите действие!",
        reply_markup=main_menu()
    )
