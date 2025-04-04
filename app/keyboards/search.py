from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.pagination_utils import build_paginated_keyboard
from utils.utils import get_actor_hash


def make_actor_movie_row_generator(actor_hash: str):
    """
    Возвращает функцию-генератор, которая для каждого фильма создаёт строку с кнопкой.
    """

    def generator(movie: dict, index: int):
        text = f"{movie['title']} ({movie.get('release_date', '❓')[:4]})"
        callback_data = f"movie_{index}_{actor_hash}"
        return [InlineKeyboardButton(text=text, callback_data=callback_data)]

    return generator


def actor_movies_keyboard(
    movies: list, actor_hash: str, page: int = 0, movies_per_page: int = 5
) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру с фильмами актёра и кнопками пагинации.
    """
    item_generator = make_actor_movie_row_generator(actor_hash)
    extra = [[InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]]
    return build_paginated_keyboard(
        data=movies,
        per_page=movies_per_page,
        page=page,
        callback_prefix=f"actor_movies_{actor_hash}",
        item_row_generator=item_generator,
        extra_buttons=extra,
    )


def movie_details_keyboard(
    movie: dict, actor_hash: str = None, page: int = 0
) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру для просмотра деталей фильма.

    - Кнопка "🎬 Подробнее на TMDB" открывает ссылку movie["tmdb_url"].
    - Кнопка "🔙 Назад" появляется только при поиске по актёру.
    """
    buttons = [
        [InlineKeyboardButton(text="🎬 Подробнее на TMDB", url=movie["tmdb_url"])]
    ]

    if actor_hash:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=f"back_to_movie_list_{actor_hash}_{page}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
