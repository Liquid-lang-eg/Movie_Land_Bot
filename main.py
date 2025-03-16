import asyncio
import uvicorn
from app.bot.bot_main import start_bot
from app.api.fastapi_main import run_api
from app.core.redis import redis_cache


async def main():
    await redis_cache.connect()

    bot_task = asyncio.create_task(start_bot())
    api_task = asyncio.create_task(run_api())

    try:
        await asyncio.gather(bot_task, api_task)
    except Exception as e:
        print(f"Ошибка: {e}")
        bot_task.cancel()
        api_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())