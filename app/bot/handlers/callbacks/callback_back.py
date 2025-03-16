from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

def some_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])
    return keyboard
