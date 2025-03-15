from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.bot.backend_requests import fetch_from_backend
from app.core.redis import redis_cache
from app.bot.keyboards.inline import actor_movies_keyboard, movie_details_keyboard, get_actor_hash

router = Router()
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
MOVIES_PER_PAGE = 5  # Количество фильмов на страницу

class SearchState(StatesGroup):
    movie_title = State()
    actor_name = State()

@router.message(SearchState.actor_name)
async def get_actor_movies_handler(message: Message, state: FSMContext):
    """Обрабатывает ввод имени актёра с кэшированием"""
    actor_name = message.text.strip().lower()

    if not actor_name:
        await message.answer("⚠ Введите корректное имя актера.")
        return

    actor_hash = get_actor_hash(actor_name)
    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)

    if not movies:
        try:
            movies = await fetch_from_backend("/actors/movies/", {"name": actor_name})
            if movies:
                await redis_cache.set(cache_key, movies, expire=86400)  # Кэшируем список фильмов на 1 день
        except Exception as e:
            await message.answer(f"❌ Ошибка при получении данных: {str(e)}")
            await state.clear()
            return

    await state.clear()

    if not movies:
        await message.answer(f"🎬 У {actor_name} нет фильмов в базе.")
        return

    keyboard = actor_movies_keyboard(movies, actor_name)
    await message.answer(f"🎬 Фильмы с {actor_name}:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("movie_"))
async def send_movie_details(callback: CallbackQuery):
    """Отправляет информацию о фильме при нажатии на кнопку"""
    try:
        # Извлекаем movie_index и actor_hash; разделяем только по первым двум символам '_'
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
        f"📖 {movie.get('description', 'Описание отсутствует.')}"
    )

    poster_url = movie.get("poster_path")
    if poster_url:
        poster_url = f"{TMDB_IMAGE_BASE_URL}{poster_url}"
        await callback.message.answer_photo(photo=poster_url, caption=caption, parse_mode="Markdown",
                                            reply_markup=movie_details_keyboard(movie))
    else:
        await callback.message.answer(caption, parse_mode="Markdown", reply_markup=movie_details_keyboard(movie))

    await callback.answer()

@router.callback_query(F.data.startswith("next_page_"))
async def send_next_page(callback: CallbackQuery):
    """Отправляет следующую страницу фильмов"""
    try:
        _, page, actor_hash = callback.data.split("_", 2)
        page = int(page)
    except Exception:
        await callback.answer("⚠ Некорректные данные, попробуйте снова.")
        return

    cache_key = f"actor_movies:{actor_hash}"
    movies = await redis_cache.get(cache_key)

    if not movies:
        await callback.answer("⚠ Данные устарели, попробуйте снова.")
        return

    # Передаем actor_hash в качестве идентификатора – функция в inline проверит, что это уже хэш
    keyboard = actor_movies_keyboard(movies, actor_hash, page)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()
