from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from app.keyboards.inline import main_menu

router = Router()

@router.callback_query(F.data == "back_to_menu")
async def back_handler(callback: CallbackQuery):
    """
    Обработчик кнопки 'Назад'. Возвращает пользователя в главное меню.
    Проверяет, содержит ли сообщение текст или подпись.
    """
    new_text = "Главное меню"
    new_markup = main_menu()

    if callback.message.text:
        await callback.message.edit_text(new_text, reply_markup=new_markup)
    elif callback.message.caption:
        await callback.message.edit_caption(new_text, reply_markup=new_markup)
    else:
        await callback.answer("Ошибка: Невозможно обновить сообщение.", show_alert=True)
