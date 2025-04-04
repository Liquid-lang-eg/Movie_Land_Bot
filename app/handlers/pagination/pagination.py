from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil


def paginate(data, page, per_page):
    total_pages = max(1, ceil(len(data) / per_page))
    start_index = page * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]
    return page_data, total_pages

def pagination_keyboard(callback_prefix: str, current_page: int, total_pages: int, extra_buttons=None):
    buttons = []

    if total_pages > 1:
        pagination_row = []
        if current_page > 0:
            pagination_row.append(
                InlineKeyboardButton(text="⬅ Назад", callback_data=f"{callback_prefix}_page_{current_page - 1}")
            )
        pagination_row.append(
            InlineKeyboardButton(text=f"{current_page + 1}/{total_pages}", callback_data="noop")
        )
        if current_page < total_pages - 1:
            pagination_row.append(
                InlineKeyboardButton(text="➡ Вперёд", callback_data=f"{callback_prefix}_page_{current_page + 1}")
            )
        buttons.append(pagination_row)

    if extra_buttons:
        buttons.extend(extra_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)