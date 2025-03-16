from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.bot.utils import get_actor_hash

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Получить рекомендации", callback_data="recommend")],
        [InlineKeyboardButton(text="🔔 Подписаться на жанр", callback_data="subscribe_genre")],
        [InlineKeyboardButton(text="🔍 Найти фильм", callback_data="search_movie_by_title")],
        [InlineKeyboardButton(text="🔍 Найти фильмы по актеру", callback_data="search_movie_by_actor")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu")]
    ])



