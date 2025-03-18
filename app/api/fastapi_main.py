from fastapi import FastAPI
from app.db.fetch_genres import fetch_genres
import uvicorn
from .routers import recommends, for_search, auth, subscriptions, genre_ids
from app.core.redis import redis_cache
import asyncio
from app.api.load_cash import load_movie_ids_into_redis


app = FastAPI()

app.include_router(recommends.router)
app.include_router(auth.router)
app.include_router(for_search.router)
app.include_router(subscriptions.router)
app.include_router(genre_ids.router)



# @app.on_event("startup")
# async def startup_event():
#     await fetch_genres()
#
# @app.on_event("startup")
# async def startup_event():
#     await redis_cache.connect()
#     asyncio.create_task(load_movie_ids_into_redis())

@app.on_event("shutdown")
async def shutdown_event():
    await redis_cache.close()

async def run_api():
    """Асинхронный запуск Uvicorn"""
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    await server.serve()