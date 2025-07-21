from typing import Annotated

from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_tool.depend import Depend
from aiogram_tool.limit import Limit

from bot.db.models import User
from bot.db.session import async_db_session
from bot.handlers.dependency import get_user, get_user_rel
from bot.utils.buttons.inline import settings_button
from bot.utils.filter.state import SkinSearchState

command_router = Router(name="command_router")



@command_router.message(Command("start"))
async def start(
     message: Message,
     _: Annotated[User, Depend(get_user)]
):
     await message.answer(
          "Я - бот, который поможет тебе отслеживать цены предметов CS2. Пропиши команду /help"
     )
     
     

@command_router.message(Command("settings"), Limit(seconds=1))
async def settings(
     message: Message,
     user: Annotated[User, Depend(get_user)]
):
     await message.answer(
          text="Настройки",
          reply_markup=await settings_button(
               steam_tied=True if user.steam_id else False
          )
     )
     
     
   
@command_router.message(Command("skip"))
async def skip(
     message: Message,
     state: FSMContext
):
     get_state = await state.get_state()
     if get_state is not None:
          await state.clear()
          return await message.answer("Событие пропущено")
     return await message.answer("Событий не найдено")



@command_router.message(Command("skin_search"), Limit(minutes=1))
async def skin_search(
     message: Message,
     state: FSMContext
):
     await state.set_state(SkinSearchState.skin)
     await message.answer("Отправь название скина")
     
    
     
@command_router.message(Command("inventory"), Limit(seconds=3))
async def inventory(
     message: Message,
     user: Annotated[User, Depend(get_user)],
):
     ...
     
     
     
@command_router.message(Command("help"))
async def help(message: Message):
     ...

    
     
     
@command_router.message(Command("skin_price_history"), Limit(seconds=5))
async def skin_price_history(
     message: Message,
     user: Annotated[User, Depend(get_user)]
):
     ...
     
     
     
@command_router.message(Command("steam_profile"))
async def steam_profile(
     message: Message,
     user: Annotated[User, Depend(get_user)]
):
     ...