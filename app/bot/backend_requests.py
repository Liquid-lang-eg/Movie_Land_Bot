from aiohttp import ClientSession
from config import BACKEND_URL

async def fetch_from_backend(endpoint: str, params: dict = None, method: str = "GET", data: dict = None):
    url = f"{BACKEND_URL}{endpoint}"
    async with aiohttp.ClientSession() as session:
        if method.upper() == "GET":
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    raise Exception(f"Ошибка при запросе к бэкенду: {response.status}")
        elif method.upper() == "POST":
            async with session.post(url, json=data, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    raise Exception(f"Ошибка при запросе к бэкенду: {response.status}")
        else:
            raise Exception("Unsupported HTTP method")


async def get_actor_movies(actor_name: str):
    """Получает список фильмов актера с описанием и постерами"""
    movies = await fetch_from_backend("/actors/movies/", {"name": actor_name})
    if not movies:
        return None

    enriched_movies = []
    for movie in movies:
        movie_data = {
            "title": movie["title"],
            "release_date": movie.get("release_date", "❓"),
            "tmdb_url": movie["tmdb_url"],
            "poster_url": movie.get("poster_url", "❌ Нет постера"),
            "overview": movie.get("'overview'", "❌ Нет описания")
        }

        enriched_movies.append(movie_data)

    return enriched_movies


async def register_user_in_backend(tg_id: int) -> dict:
    payload = {"tg_id": tg_id}
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/auth/register", json=payload) as resp:
            if resp.headers.get("Content-Type", "").startswith("application/json"):
                return await resp.json()
            else:
                text = await resp.text()
                return {"error": f"Сервер вернул статус {resp.status}", "details": text}

import aiohttp
from config import BACKEND_URL


async def get_genres():
    return await fetch_from_backend("/subscription/genres/")


async def get_user_subscriptions(tg_id: int):
    params = {"user_tg_id": tg_id}
    return await fetch_from_backend("/subscription/subscriptions/", params=params)


async def subscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/subscribe/", method="POST", data=data)


async def unsubscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/unsubscribe/", method="POST", data=data)
