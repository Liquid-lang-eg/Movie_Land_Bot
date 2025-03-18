from fastapi import APIRouter, HTTPException, Query
from app.bot.backend_requests import fetch_from_backend
from app.core.redis import redis_cache
import logging
from config import MAX_ERROR_LENGTH

router = APIRouter(prefix="/movies", tags=["movies"])

logger = logging.getLogger(__name__)

EMPTY_MARKER = "__empty__"


@router.get("/genre_ids/")
async def get_movie_ids_for_genre(genre_id: int = Query(...)):
    key = f"movies:genre:{genre_id}:ids"
    movie_ids = await redis_cache.get(key)

    if movie_ids is not None:
        if movie_ids == EMPTY_MARKER:
            raise HTTPException(status_code=404, detail="ID фильмов не найдены для данного жанра")
        return {"genre_id": genre_id, "movie_ids": movie_ids}

    params = {"genre_id": genre_id}
    try:
        movie_ids = await fetch_from_backend("/movies/genre_ids/", method="GET", params=params)
    except Exception as e:
        # Логируем полную ошибку, но отправляем клиенту сокращённое сообщение
        logger.exception(f"Ошибка получения данных для жанра {genre_id}")
        error_detail = str(e)[:MAX_ERROR_LENGTH]
        await redis_cache.set(key, EMPTY_MARKER, expire=86400)
        raise HTTPException(status_code=500, detail=f"Ошибка получения данных: {error_detail}")

    if not movie_ids:
        await redis_cache.set(key, EMPTY_MARKER, expire=86400)
        raise HTTPException(status_code=404, detail="ID фильмов не найдены для данного жанра")

    try:
        sorted_ids = sorted(movie_ids)
    except Exception as e:
        logger.exception("Ошибка сортировки данных")
        await redis_cache.set(key, EMPTY_MARKER, expire=86400)
        raise HTTPException(status_code=500, detail="Ошибка сортировки данных")

    await redis_cache.set(key, sorted_ids, expire=86400)
    return {"genre_id": genre_id, "movie_ids": sorted_ids}