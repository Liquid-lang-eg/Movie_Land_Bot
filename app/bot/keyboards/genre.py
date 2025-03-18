from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.utils.pagination_utils import build_paginated_keyboard

def make_genre_row_generator(user_genre_ids: set):
    """
    Возвращает функцию-генератор, которая для каждого жанра создаёт строку с кнопкой.
    """
    def generator(genre: dict, index: int):
        check = "✅ " if genre["id"] in user_genre_ids else ""
        text = f"{check}{genre['name']}"
        callback_data = f"subscribe_{genre['id']}"
        return [InlineKeyboardButton(text=text, callback_data=callback_data)]
    return generator


def genre_subscription_keyboard(genres: list, user_genre_ids: set, page: int = 0, per_page: int = 6) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру для подписки на жанры с пагинацией.
    """
    item_generator = make_genre_row_generator(user_genre_ids)
    extra = [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]]
    return build_paginated_keyboard(
        data=genres,
        per_page=per_page,
        page=page,
        callback_prefix="genre",
        item_row_generator=item_generator,
        extra_buttons=extra
    )