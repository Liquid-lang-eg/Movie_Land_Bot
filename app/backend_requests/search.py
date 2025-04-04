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