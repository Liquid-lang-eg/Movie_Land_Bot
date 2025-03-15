from fastapi import FastAPI
from app.db.fetch_genres import fetch_genres
import uvicorn
from .routers import recommends, for_search, auth
app = FastAPI()

app.include_router(recommends.router)
app.include_router(auth.router)
app.include_router(for_search.router)
@app.on_event("startup")
async def startup_event():
    await fetch_genres()


async def run_api():
    """Асинхронный запуск Uvicorn"""
    config = uvicorn.Config(app, host="127.0.0.1", port=8000)
    server = uvicorn.Server(config)
    await server.serve()