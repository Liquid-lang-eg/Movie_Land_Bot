import aiohttp
from app.db.models import Genre
from app.db.conn import get_db
from config import TMDB_API_KEY

TMDB_API_URL = "https://api.themoviedb.org/3/genre/movie/list"

async def fetch_genres():
    """Получает список жанров из TMDB и сохраняет в БД при старте сервера."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{TMDB_API_URL}?api_key={TMDB_API_KEY}&language=ru-RU") as resp:
            data = await resp.json()
            genres = data.get("genres", [])

    async for db in get_db():
        for genre in genres:
            existing_genre = await db.get(Genre, genre["id"])
            if not existing_genre:
                db.add(Genre(id=genre["id"], name=genre["name"]))
        await db.commit()
        break
