from aiogram import Router
from aiogram.types import CallbackQuery
from config import BACKEND_URL
from aiohttp import ClientSession

router = Router()

@router.callback_query(lambda c: c.data == "subscribe_genre")
async def subscribe_genre(callback: CallbackQuery):
    """Отправляет запрос на подписку через FastAPI."""
    async with ClientSession() as session:
        async with session.post(f"{BACKEND_URL}/subscriptions/subscribe", json={
            "user_id": callback.from_user.id,
            "genre_id": 1
        }) as resp:
            data = await resp.json()
            await callback.message.answer(data.get("message", "✅ Вы подписались на жанр!"))
    await callback.answer()