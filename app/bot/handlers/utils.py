TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

async def get_movie_poster(movie):
    """Возвращает URL постера фильма, если он есть"""
    poster_path = movie.get("poster_path")
    if not poster_path:
        return None
    return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
