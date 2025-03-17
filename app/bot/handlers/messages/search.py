from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from app.bot.backend_requests import fetch_from_backend
from app.core.redis import redis_cache
from app.bot.keyboards.search import actor_movies_keyboard, movie_details_keyboard, get_actor_hash
from app.bot.utils.pagination_utils import build_paginated_keyboard  # если нужно отдельно
from aiogram.fsm.state import State, StatesGroup

router = Router()
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
MOVIES_PER_PAGE = 5  # Количество фильмов на страницу

class SearchState(StatesGroup):
    movie_title = State()
    actor_name = State()

@router.message(SearchState.actor_name)
async def get_actor_movies_handler(message: Message, state: FSMContext):
    actor_name = message.text.strip().lower()
    if not actor_name:
        await message.answer("⚠ Введите корректное имя актера.")
        return

    # Вычисляем хэш один раз
    actor_hash = get_actor_hash(actor_name)
    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)

    if not movies:
        try:
            movies = await fetch_from_backend("/actors/movies/", {"name": actor_name})
            if movies:
                await redis_cache.set(cache_key, movies, expire=86400)
        except Exception as e:
            await message.answer(f"❌ Ошибка при получении данных: {str(e)}")
            await state.clear()
            return

    await state.clear()

    if not movies:
        await message.answer(f"🎬 У {actor_name} нет фильмов в базе.")
        return

    # Передаём actor_hash вместо actor_name
    keyboard = actor_movies_keyboard(movies, actor_hash, page=0, movies_per_page=MOVIES_PER_PAGE)
    await message.answer(f"🎬 Фильмы с {actor_name}:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("actor_movies_"))
async def paginate_actor_movies(callback: CallbackQuery):
    """
    Обрабатывает нажатия кнопок пагинации для списка фильмов актёра.
    Ожидается формат callback_data: "actor_movies_<actor_hash>_page_<page>"
    """
    try:
        # Используем rsplit, чтобы извлечь последний элемент как номер страницы.
        parts = callback.data.rsplit("_", 1)
        page = int(parts[1])
        # Извлекаем actor_hash из второй части: формат "actor_movies_<actor_hash>"
        actor_hash = parts[0].split("_")[2]
    except Exception:
        await callback.answer("Ошибка данных, попробуйте снова.")
        return

    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)
    if not movies:
        await callback.answer("Данные устарели, попробуйте снова.")
        return

    keyboard = actor_movies_keyboard(movies, actor_hash, page, MOVIES_PER_PAGE)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("movie_"))
async def send_movie_details(callback: CallbackQuery):
    """
    Отправляет информацию о фильме при нажатии на кнопку.
    Ожидается формат callback_data: "movie_<movie_index>_<actor_hash>"
    """
    try:
        _, movie_index, actor_hash = callback.data.split("_", 2)
        movie_index = int(movie_index)
    except Exception:
        await callback.answer("⚠ Некорректные данные, попробуйте снова.")
        return

    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)
    if not movies or movie_index >= len(movies):
        await callback.answer("⚠ Данные устарели, попробуйте снова.")
        return

    movie = movies[movie_index]
    caption = (
        f"🎬 [{movie['title']} ({movie.get('release_date', '❓')[:4]})]({movie['tmdb_url']})\n\n"
        f"📖 {movie.get('overview', 'Описание отсутствует.')}"
    )

    poster_url = movie.get("poster_path")
    if poster_url:
        poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_url}"
        await callback.message.answer_photo(
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=movie_details_keyboard(movie, actor_hash, page=0)
        )
    else:
        await callback.message.answer(
            caption,
            parse_mode="Markdown",
            reply_markup=movie_details_keyboard(movie, actor_hash, page=0)
        )
    await callback.answer()

@router.callback_query(F.data.startswith("next_page_"))
async def send_next_page(callback: CallbackQuery):
    """
    Обрабатывает кнопку "Следующая страница" для списка фильмов актёра.
    Ожидается формат callback_data: "next_page_<page>_<actor_hash>"
    """
    try:
        _, page_str, actor_hash = callback.data.split("_", 2)
        page = int(page_str)
    except Exception:
        await callback.answer("⚠ Некорректные данные, попробуйте снова.")
        return

    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)
    if not movies:
        await callback.answer("⚠ Данные устарели, попробуйте снова.")
        return

    keyboard = actor_movies_keyboard(movies, actor_hash, page, MOVIES_PER_PAGE)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("back_to_movie_list_"))
async def back_to_movie_list(callback: CallbackQuery):
    """
    Обрабатывает кнопку "Назад" в деталях фильма и возвращает меню с выбором фильмов.
    Ожидается формат callback_data: "back_to_movie_list_<actor_hash>_<page>"
    """
    try:
        _, actor_hash, page_str = callback.data.split("_", 2)
        page = int(page_str)
    except Exception:
        await callback.answer("Ошибка данных, попробуйте снова.", show_alert=True)
        return

    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)
    if not movies:
        await callback.answer("Данные устарели, попробуйте снова.", show_alert=True)
        return

    keyboard = actor_movies_keyboard(movies, actor_hash, page, MOVIES_PER_PAGE)
    # Если текущее сообщение не содержит текста, обновляем caption или отправляем новое сообщение
    if callback.message.text:
        await callback.message.edit_text("🎬 Выберите фильм:", reply_markup=keyboard)
    elif callback.message.caption:
        await callback.message.edit_caption("🎬 Выберите фильм:", reply_markup=keyboard)
    else:
        await callback.message.answer("🎬 Выберите фильм:", reply_markup=keyboard)
    await callback.answer()


