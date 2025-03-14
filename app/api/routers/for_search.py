import aiohttp
import urllib.parse
from fastapi import APIRouter, HTTPException
from config import TMDB_API_KEY

router = APIRouter()

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/person"
TMDB_MOVIE_CREDITS_URL = "https://api.themoviedb.org/3/person/{actor_id}/movie_credits"

@router.get("/actors/movies/")
async def get_actor_movies(name: str):
    """Получает список фильмов с актером, сортирует и добавляет ссылки"""
    encoded_name = urllib.parse.quote_plus(name)

    async with aiohttp.ClientSession() as session:

        async with session.get(
            f"{TMDB_SEARCH_URL}?api_key={TMDB_API_KEY}&query={encoded_name}&language=ru-RU"
        ) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Ошибка поиска актера")

            data = await resp.json()
            results = data.get("results", [])

            if not results:
                raise HTTPException(status_code=404, detail=f"Актер '{name}' не найден")

            actor_id = results[0]["id"]

        async with session.get(
            TMDB_MOVIE_CREDITS_URL.format(actor_id=actor_id) + f"?api_key={TMDB_API_KEY}&language=ru-RU"
        ) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Ошибка загрузки фильмов")

            movies = await resp.json()
            movie_list = movies.get("cast", [])

            movie_list = sorted(
                [m for m in movie_list if m.get("release_date")],
                key=lambda x: x["release_date"],
                reverse=True
            )
            print(movie_list.pop())
            for movie in movie_list:
                movie["tmdb_url"] = f"https://www.themoviedb.org/movie/{movie['id']}"

            return movie_list

@router.get("/movies/search/")
async def search_movie(title: str):
    """Ищет фильм по названию и возвращает его данные"""
    encoded_title = urllib.parse.quote_plus(title)

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{TMDB_SEARCH_URL}?api_key={TMDB_API_KEY}&query={encoded_title}&language=ru-RU"
        ) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=resp.status, detail="Ошибка поиска фильма")

            data = await resp.json()
            results = data.get("results", [])

            if not results:
                raise HTTPException(status_code=404, detail=f"Фильм '{title}' не найден")

            movie = results[0]
            print(movie)
            movie["tmdb_url"] = f"https://www.themoviedb.org/movie/{movie['id']}"

            return movie