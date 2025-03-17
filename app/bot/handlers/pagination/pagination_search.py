from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.core.redis import redis_cache
from app.bot.keyboards.search import actor_movies_keyboard, movie_details_keyboard

router = Router()
MOVIES_PER_PAGE = 5

@router.callback_query(F.data.startswith("actor_movies_page_"))
async def paginate_actor_movies(callback: CallbackQuery):
    try:
        _, _, actor_hash, page_str = callback.data.split("_")
        page = int(page_str)
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
    try:
        # Ожидается формат: "movie_<movie_index>_<actor_hash>"
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
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}"
        await callback.message.answer_photo(
            photo=poster_url,
            caption=caption,
            parse_mode="Markdown",
            reply_markup=movie_details_keyboard(movie)
        )
    else:
        await callback.message.answer(
            caption,
            parse_mode="Markdown",
            reply_markup=movie_details_keyboard(movie)
        )
    await callback.answer()

@router.callback_query(F.data.startswith("next_page_"))
async def send_next_page(callback: CallbackQuery):
    try:
        # Ожидается формат: "next_page_<page>_<actor_hash>"
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
