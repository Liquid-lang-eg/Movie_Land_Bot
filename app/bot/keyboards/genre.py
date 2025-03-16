from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def genre_subscription_keyboard(genres: list, user_subscriptions: set) -> InlineKeyboardMarkup:
    """
    genres: список жанров в виде словарей с ключами 'id' и 'name'
    user_subscriptions: множество id жанров, на которые подписан пользователь
    """
    buttons = []
    for genre in genres:
        genre_id = genre["id"]
        subscribed = genre_id in user_subscriptions
        text = f"{genre['name']} — {'Отписаться' if subscribed else 'Подписаться'}"
        callback_data = f"{'unsubscribe' if subscribed else 'subscribe'}_{genre_id}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=callback_data)])
    buttons.append([InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)