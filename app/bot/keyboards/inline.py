from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import hashlib

def get_actor_hash(actor_name: str) -> str:
    """Возвращает MD5-хэш от имени актёра (в нижнем регистре)"""
    return hashlib.md5(actor_name.lower().encode()).hexdigest()

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Получить рекомендации", callback_data="recommend")],
        [InlineKeyboardButton(text="🔔 Подписаться на жанр", callback_data="subscribe_genre")],
        [InlineKeyboardButton(text="🔍 Найти фильм", callback_data="search_movie_by_title")],
        [InlineKeyboardButton(text="🔍 Найти фильмы по актеру", callback_data="search_movie_by_actor")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu")]
    ])

def actor_movies_keyboard(movies, actor_name, page=0, movies_per_page=5):
    """Генерирует клавиатуру с фильмами актера"""
    start_index = page * movies_per_page
    end_index = start_index + movies_per_page
    next_page = page + 1

    # Вместо передачи полного имени используем его хэш для соблюдения ограничений Telegram
    actor_hash = get_actor_hash(actor_name)

    buttons = [
        [InlineKeyboardButton(
            text=f"{movie['title']} ({movie.get('release_date', '❓')[:4]})",
            callback_data=f"movie_{i}_{actor_hash}"
        )]
        for i, movie in enumerate(movies[start_index:end_index], start=start_index)
    ]

    if end_index < len(movies):
        buttons.append([InlineKeyboardButton(
            text="➡ Еще",
            callback_data=f"next_page_{next_page}_{actor_hash}"
        )])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def movie_details_keyboard(movie):
    """Кнопка с кликабельной ссылкой на фильм"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎬 Подробнее на TMDB", url=movie["tmdb_url"])]
    ])