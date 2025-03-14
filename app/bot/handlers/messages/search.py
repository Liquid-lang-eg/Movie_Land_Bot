from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.bot.backend_requests import fetch_from_backend

router = Router()
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

MOVIES_PER_PAGE = 5
USER_MOVIE_CACHE = {} # - заглушка в итоговом варианте будет подключен redis

class SearchState(StatesGroup):
    movie_title = State()
    actor_name = State()



@router.message(SearchState.movie_title)
async def get_movie_handler(message: Message, state: FSMContext):
    """Обрабатывает ввод названия фильма"""
    movie_title = message.text.strip()

    if not movie_title:
        await message.answer("⚠ Введите корректное название фильма.")
        return

    try:
        movie = await fetch_from_backend("/movies/search/", {"title": movie_title})
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении данных: {str(e)}")
        await state.clear()
        return

    await state.clear()

    if not movie:
        await message.answer(f"🚫 Фильм '{movie_title}' не найден.")
        return

    caption = (
        f"🎬 [{movie['title']} ({movie.get('release_date', '❓')[:4]})]({movie['tmdb_url']})\n\n"
        f"📖 {movie.get('overview', 'Описание отсутствует.')}"
    )

    poster_url = movie.get("poster_path")
    if poster_url:
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_url}"
        await message.answer_photo(photo=poster_url, caption=caption, parse_mode="Markdown")
    else:
        await message.answer(caption, parse_mode="Markdown")

@router.message(SearchState.actor_name)
async def get_actor_movies_handler(message: Message, state: FSMContext):
    """Обрабатывает ввод имени актёра"""
    actor_name = message.text.strip()

    if not actor_name:
        await message.answer("⚠ Введите корректное имя актера.")
        return

    try:
        movies = await fetch_from_backend("/actors/movies/", {"name": actor_name})
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении данных: {str(e)}")
        await state.clear()
        return

    await state.clear()

    if not movies:
        await message.answer(f"🎬 У {actor_name} нет фильмов в базе.")
        return

    USER_MOVIE_CACHE[message.from_user.id] = movies

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{movie['title']} ({movie.get('release_date', '❓')[:4]})",
                                  callback_data=f"movie_{i}")]
            for i, movie in enumerate(movies[:10])
        ]
    )

    await message.answer(f"🎬 Фильмы с {actor_name}:", reply_markup=keyboard)





