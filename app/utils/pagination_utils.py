from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from math import ceil

def build_paginated_keyboard(
    data,
    per_page: int,
    page: int,
    callback_prefix: str,
    item_row_generator,
    extra_buttons: list = None
) -> InlineKeyboardMarkup:
    """
    Строит пагинированную inline-клавиатуру для заданного списка элементов.

    :param data: Список элементов, которые нужно отобразить.
    :param per_page: Количество элементов на одну страницу.
    :param page: Номер текущей страницы (начинается с 0).
    :param callback_prefix: Префикс для callback_data кнопок пагинации.
    :param item_row_generator: Функция, принимающая (item, global_index) и возвращающая список InlineKeyboardButton (одна строка).
    :param extra_buttons: Дополнительные кнопки (список строк кнопок), которые будут добавлены ниже пагинации.
    :return: InlineKeyboardMarkup с построенной клавиатурой.
    """
    total_pages = max(1, ceil(len(data) / per_page))
    start_index = page * per_page
    end_index = start_index + per_page
    page_data = data[start_index:end_index]

    keyboard_rows = []
    for i, item in enumerate(page_data, start=start_index):
        row = item_row_generator(item, i)
        if row:
            keyboard_rows.append(row)

    pagination_row = []
    if page > 0:
        pagination_row.append(
            InlineKeyboardButton(text="⬅ Назад", callback_data=f"{callback_prefix}_page_{page - 1}")
        )
    pagination_row.append(
        InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop")
    )
    if page < total_pages - 1:
        pagination_row.append(
            InlineKeyboardButton(text="➡ Вперёд", callback_data=f"{callback_prefix}_page_{page + 1}")
        )
    keyboard_rows.append(pagination_row)

    if extra_buttons:
        keyboard_rows.extend(extra_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard_rows)