from aiohttp import ClientSession
from config import BACKEND_URL

async def fetch_from_backend(endpoint: str, params: dict = None):
    """Запрашивает данные с FastAPI"""
    url = f"{BACKEND_URL}{endpoint}"
    async with ClientSession() as session:
        async with session.get(url, params=params) as response:

            if response.status == 200:
                return await response.json()
            elif response.status == 404:
                return None
            else:
                raise Exception(f"Ошибка при запросе к бэкенду: {response.status}")


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
                # Здесь можно залогировать ошибку или вернуть словарь с описанием ошибки
                return {"error": f"Сервер вернул статус {resp.status}", "details": text}
