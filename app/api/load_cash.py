from app.core.redis import redis_cache

async def load_movie_ids_into_redis():
    """
    Для каждого жанра запрашивает ID фильмов постранично (fetch_all_movie_ids_for_genre)
    и сохраняет итоговый список в Redis.
    """
    genres = await get_genres()
    if not genres:
        print("Жанры не найдены")
        return

    for genre in genres:
        genre_id = genre["id"]
        try:
            # Получаем все ID фильмов по жанру.
            movie_ids = await fetch_all_movie_ids_for_genre(genre_id)
        except Exception as e:
            print(f"Ошибка получения ID фильмов для жанра {genre_id}: {e}")
            continue

        if movie_ids:
            sorted_ids = sorted(movie_ids)
            key = f"movies:genre:{genre_id}:ids"
            await redis_cache.set(key, sorted_ids, expire=86400)
            print(f"Кэшировано {len(sorted_ids)} ID фильмов для жанра {genre_id}")
        else:
            print(f"Для жанра {genre_id} не получены ID фильмов")