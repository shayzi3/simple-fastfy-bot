from typing import Annotated

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram_tool.depend import Depend
from aiogram_tool.limit import Limit
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.session import async_db_session
from bot.handlers.dependency import get_user, get_user_rel
from bot.responses import isresponse
from bot.utils.buttons.inline import inventory_button, settings_button
from bot.utils.compress import CompressSkinName
from bot.utils.filter.state import SkinSearchState

from .service import CommandService, get_command_service

command_router = Router(name="command_router")



@command_router.message(Command("start"), Limit(seconds=3))
async def start(
     message: Message,
     _: Annotated[User, Depend(get_user)]
):
     await message.answer(
          "Я - бот, который поможет тебе отслеживать цены предметов CS2. Пропиши команду /help"
     )
     
     

@command_router.message(Command("settings"), Limit(seconds=3))
async def settings(
     message: Message,
     user: Annotated[User, Depend(get_user)]
):
     # steam profile
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



@command_router.message(Command("skin_search"), Limit(seconds=30))
async def skin_search(
     message: Message,
     state: FSMContext
):
     await state.set_state(SkinSearchState.skin)
     await message.answer("Отправь название скина")
     
    

@command_router.message(Command("inventory"), Limit(seconds=5))
async def inventory(
     message: Message,
     user: Annotated[User, Depend(get_user_rel)],
):
     if not user.skins:
          return await message.answer("Ваш инвентарь пуст")
     
     await message.answer(
          text="Инвентарь",
          reply_markup=await inventory_button(
               skins=[
                    CompressSkinName.compress(
                         name=skin.skin_name,
                         from_compress=False
                    ) for skin in user.skins
               ]
          )
     )
     
     
     
     
@command_router.message(Command("help"))
async def help(message: Message):
     ...

    
     
     
@command_router.message(Command("skin_price_history"), Limit(seconds=3))
async def skin_price_history(
     message: Message,
     user: Annotated[User, Depend(get_user)]
):
     ...
     
     

@command_router.message(Command("skins_from_steam"), Limit(minutes=10))
async def skins_from_steam(
     message: Message,
     user: Annotated[User, Depend(get_user_rel)],
     session: Annotated[AsyncSession, Depend(async_db_session)],
     service: Annotated[CommandService, Depend(get_command_service)]
):
     if not user.steam_id:
          return await message.answer("Для использования этой команды нужно привязать Steam. /settings")
     
     msg = await message.answer("Начинаю выгрузку предметов...")
     result = await service.skins_from_steam(
          user=user,
          session=session
     )
     if isresponse(result):
          await msg.delete()
          return await message.answer(text=result.text)
     
     await msg.delete()
     await message.answer(
          text=f"*Список добавленных предметов:* \n{result}",
          parse_mode=ParseMode.MARKDOWN_V2
     )
     
     
     