import asyncio
import logging
import logging.config
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from app.utils.logger import logging_config
from app.handlers.messages import reminders, search, start, subscribe, back_to_menu
from app.handlers.callbacks import (
    callback_search,
    callback_reminders,
    callback_subscribe,
    callback_start,
    callback_back,
)
from app.handlers.pagination import pagination_search
from app.admin.fastapi_main import start_fastapi
from config import settings


logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:
    logging.config.dictConfig(logging_config)
    logger.info("Starting BOTV")

    # Инициализируем бот, редис и диспетчер
    bot: Bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    storage = RedisStorage.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
        key_builder=DefaultKeyBuilder(with_destiny=True),
    )
    dp: Dispatcher = Dispatcher(storage=storage)

    # Регистриуем роутеры в диспетчере
    dp.include_router(start.router)
    dp.include_router(reminders.router)
    dp.include_router(subscribe.router)
    dp.include_router(search.router)
    dp.include_router(callback_search.router)
    dp.include_router(callback_reminders.router)
    dp.include_router(callback_subscribe.router)
    dp.include_router(callback_start.router)
    dp.include_router(callback_back.router)
    dp.include_router(back_to_menu.router)
    dp.include_router(pagination_search.router)

    asyncio.create_task(start_fastapi())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"[Exception] - {e}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
