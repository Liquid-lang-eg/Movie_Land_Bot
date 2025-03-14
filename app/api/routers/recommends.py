from fastapi import APIRouter
from aiohttp import ClientSession
from config import TMDB_API_KEY


router = APIRouter(prefix="/recommends", tags=["recommends"])

TMDB_API_URL = "https://api.themoviedb.org/3"


@router.get("/movies/recommend")
async def recommend_movies(user_id: int):
    async with ClientSession() as session:
        async with session.get(f"{TMDB_API_URL}/movie/popular", params={"api_key": TMDB_API_KEY}) as resp:
            data = await resp.json()
            if "results" not in data:
                return {"movies": []}

            movies = [{"title": m["title"], "year": m.get("release_date", "Неизвестно")[:4]} for m in
                      data["results"][:5]]
            return {"movies": movies}