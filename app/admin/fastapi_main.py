import uvicorn
from fastapi import FastAPI
from app.admin.view import setup_admin

app = FastAPI()
setup_admin(app)


async def start_fastapi():
    """Функция для запуска FastAPI"""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
    server = uvicorn.Server(config)
    await server.serve()
