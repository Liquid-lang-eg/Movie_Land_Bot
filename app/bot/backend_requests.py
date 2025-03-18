from aiohttp import ClientSession
from config import BACKEND_URL, MAX_ERROR_LENGTH
import asyncio

async def fetch_from_backend(
    endpoint: str,
    params: dict = None,
    method: str = "GET",
    data: dict = None,
):
    """
    Делает запрос к локальному (или любому другому) бэкенду.
    Поддерживает методы GET, POST и DELETE.
    """
    url = f"{BACKEND_URL}{endpoint}"
    if params is None:
        params = {}

    async with ClientSession() as session:
        method = method.upper()

        if method == "GET":
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        elif method == "POST":
            async with session.post(url, json=data, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        elif method == "DELETE":
            async with session.delete(url, json=data, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    return None
                else:
                    error_body = await response.text()
                    error_body = error_body[:MAX_ERROR_LENGTH]
                    raise Exception(
                        f"Ошибка при запросе к бэкенду: {response.status}. "
                        f"Тело ответа: {error_body}"
                    )
        else:
            raise Exception(f"Unsupported HTTP method: {method}")


async def fetch_all_movie_ids_for_genre(genre_id: int, max_pages: int = 10):
    """
    Делает последовательные GET-запросы к локальному эндпоинту "/movies/genre_ids/",
    чтобы получить постраничный список ID фильмов. Возвращает все ID, собранные за max_pages.
    """
    all_ids = []
    page = 1

    while page <= max_pages:
        params = {"genre_id": genre_id, "page": page}
        try:
            # Ожидаем, что бэкенд вернет список ID.
            result = await fetch_from_backend(
                "/movies/genre_ids/", method="GET", params=params
            )
        except Exception as e:
            # Если запрос не удался, прерываем цикл или логируем ошибку.
            raise Exception(f"Ошибка на странице {page}: {e}")

        if not result:
            # Пустой результат = больше страниц нет.
            break

        # Предполагаем, что result — это список ID.
        all_ids.extend(result)
        page += 1

    return all_ids


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
    print("DEBUG: get_genres() called")
    return await fetch_from_backend("/subscription/genres/")


async def get_user_subscriptions(tg_id: int):
    params = {"user_tg_id": tg_id}
    return await fetch_from_backend("/subscription/subscriptions/", params=params)


async def subscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/subscribe/", method="POST", data=data)


async def unsubscribe_genre(tg_id: int, genre_id: int):
    data = {"user_tg_id": tg_id, "genre_id": genre_id}
    return await fetch_from_backend("/subscription/unsubscribe/", method="DELETE", data=data)
