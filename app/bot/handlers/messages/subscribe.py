from aiogram import Router, F
from aiogram.types import CallbackQuery
from app.bot.backend_requests import get_genres, get_user_subscriptions, subscribe_genre, unsubscribe_genre
from app.bot.keyboards.genre import genre_subscription_keyboard
from app.bot.handlers.messages.back_to_menu import back_handler

router = Router()

@router.callback_query(F.data == "subscribe_genre")
async def show_genre_list(callback: CallbackQuery):
    """Отображает список жанров с кнопкой 'Назад'"""
    tg_id = callback.from_user.id
    genres = await get_genres()
    user_subs = await get_user_subscriptions(tg_id)
    user_genre_ids = {sub["genre_id"] for sub in user_subs} if user_subs else set()

    keyboard = genre_subscription_keyboard(genres, user_genre_ids)
    await callback.message.edit_text("Выберите жанр для подписки/отписки:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("subscribe_"))
async def handle_subscribe(callback: CallbackQuery):
    try:
        _, genre_id_str = callback.data.split("_", 1)
        genre_id = int(genre_id_str)
    except Exception:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    tg_id = callback.from_user.id
    result = await subscribe_genre(tg_id, genre_id)
    if result and result.get("detail") == "Subscribed":
        await callback.answer("Вы успешно подписались!")
    else:
        await callback.answer("Вы уже подписаны на этот жанр.")
    await show_genre_list(callback)


@router.callback_query(F.data.startswith("unsubscribe_"))
async def handle_unsubscribe(callback: CallbackQuery):
    try:
        _, genre_id_str = callback.data.split("_", 1)
        genre_id = int(genre_id_str)
    except Exception:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    tg_id = callback.from_user.id
    result = await unsubscribe_genre(tg_id, genre_id)
    if result and result.get("detail") == "Unsubscribed":
        await callback.answer("Вы успешно отписались!")
    else:
        await callback.answer("Вы не подписаны на этот жанр.")
    await show_genre_list(callback)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await back_handler(callback)