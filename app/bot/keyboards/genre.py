from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def genre_subscription_keyboard(genres, user_genre_ids):
    keyboard = [
        [InlineKeyboardButton(
            text=f"{'✅' if genre['id'] in user_genre_ids else ''} {genre['name']}",
            callback_data=f"subscribe_{genre['id']}"
        )]
        for genre in genres
    ]

    keyboard.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)