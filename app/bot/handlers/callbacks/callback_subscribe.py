from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()

class SearchState(StatesGroup):
    movie_title = State()
    actor_name = State()

@router.callback_query(F.data == "search_movie_by_title")
async def ask_movie(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название фильма:")
    await state.set_state(SearchState.movie_title)
    await callback.answer()

@router.callback_query(F.data == "search_movie_by_actor")
async def ask_movie(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название фильма:")
    await state.set_state(SearchState.movie_title)
    await callback.answer()