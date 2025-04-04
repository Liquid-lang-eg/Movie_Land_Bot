from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from app.keyboards.inline import main_menu
from app.backend_requests import (
    get_genres,
    get_user_subscriptions,
    subscribe_genre,
    unsubscribe_genre,
)
from handlers.pagination.pagination import paginate, pagination_keyboard

router = Router()
GENRES_PER_PAGE = 6


@router.callback_query(F.data == "subscribe_genre")
async def show_genre_list(callback: CallbackQuery, page: int = 0):
    """Отображает список жанров с кнопками подписки/отписки и поддержкой пагинации"""
    tg_id = callback.from_user.id
    print("DEBUG: show_genre_list called")
    genres = await get_genres()
    print(f"DEBUG: genres = {genres}")
    user_subs = await get_user_subscriptions(tg_id)
    user_genre_ids = {sub["genre_id"] for sub in user_subs} if user_subs else set()

    page_genres, total_pages = paginate(genres, page, GENRES_PER_PAGE)
    genre_buttons = [
        [
            InlineKeyboardButton(
                text=f"{'✅' if genre['id'] in user_genre_ids else ''} {genre['name']}",
                # Включаем номер страницы в callback_data
                callback_data=f"{'unsubscribe' if genre['id'] in user_genre_ids else 'subscribe'}_{genre['id']}_{page}",
            )
        ]
        for genre in page_genres
    ]

    pagination_kb = pagination_keyboard(
        "genre",
        page,
        total_pages,
        extra_buttons=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ],
    )
    final_buttons = genre_buttons + pagination_kb.inline_keyboard
    final_keyboard = InlineKeyboardMarkup(inline_keyboard=final_buttons)

    await callback.message.edit_text(
        "Выберите жанр для подписки/отписки:", reply_markup=final_keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("genre_page_"))
async def paginate_genres(callback: CallbackQuery):
    """Обрабатывает нажатия кнопок пагинации списка жанров"""
    try:
        _, page_str = callback.data.rsplit("_", 1)
        page = int(page_str)
    except ValueError:
        await callback.answer("Ошибка данных, попробуйте снова.")
        return

    await show_genre_list(callback, page)


@router.callback_query(F.data.startswith("subscribe_"))
async def handle_subscribe(callback: CallbackQuery):
    """Обрабатывает подписку на жанр, оставаясь на текущей странице"""
    try:
        # Формат callback_data: subscribe_<genre_id>_<page>
        parts = callback.data.split("_")
        genre_id = int(parts[1])
        current_page = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    tg_id = callback.from_user.id
    result = await subscribe_genre(tg_id, genre_id)
    if result and result.get("detail") == "Subscribed":
        await callback.answer("Вы успешно подписались!")
    else:
        await callback.answer("Вы уже подписаны на этот жанр.")

    # Передаем current_page вместо фиксированного 0
    await show_genre_list(callback, page=current_page)


@router.callback_query(F.data.startswith("unsubscribe_"))
async def handle_unsubscribe(callback: CallbackQuery):
    """Обрабатывает отписку от жанра, оставаясь на текущей странице"""
    try:
        # Формат callback_data: unsubscribe_<genre_id>_<page>
        parts = callback.data.split("_")
        genre_id = int(parts[1])
        current_page = int(parts[2]) if len(parts) > 2 else 0
    except ValueError:
        await callback.answer("Ошибка данных", show_alert=True)
        return

    tg_id = callback.from_user.id
    result = await unsubscribe_genre(tg_id, genre_id)
    if result and result.get("detail") == "Unsubscribed":
        await callback.answer("Вы успешно отписались!")
    else:
        await callback.answer("Вы не подписаны на этот жанр.")

    await show_genre_list(callback, page=current_page)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):

    await callback.message.edit_text("Главное меню", reply_markup=main_menu())
    await callback.answer()
