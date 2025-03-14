import asyncio
import uvicorn
from app.bot.bot_main import start_bot
from app.api.fastapi_main import run_api

async def main():
    bot_task = asyncio.create_task(start_bot())  # Запуск бота
    api_task = asyncio.create_task(run_api())  # Запуск API
    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    asyncio.run(main())