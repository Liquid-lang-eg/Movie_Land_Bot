from aiogram import Dispatcher
from .handlers.messages import reminders, search, start, subscribe, back_to_menu
from .handlers.callbacks import callback_search, callback_reminders, callback_subscribe, callback_start, callback_back

def setup_routers(dp: Dispatcher):
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