from typing import Annotated

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.utils.markdown import link
from aiogram_tool.depend import Depend
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.session import async_db_session
from bot.handlers.dependency import get_user
from bot.responses import isresponse
from bot.utils.buttons.inline import steam_profile_button, steam_skins_button
from bot.utils.filter.state import SkinPercentState, SkinSearchState, SteamIDState

from .service import StateService, get_state_service

state_router = Router(name="state_router")


     
@state_router.message(SkinSearchState.skin)
async def skin_search(
     message: Message,
     state: FSMContext,
     service: Annotated[StateService, Depend(get_state_service)]
):
     result = await service.skin_search(query=message.text)
     if isresponse(result):
          text = result.text
          if getattr(result, "__name__", "") == "SkinNotFound":
               text = result.text.format(message.text)
          return await message.answer(text=text)
     
     await message.answer(
          text=f"Предметы по запросу: {message.text}",
          reply_markup=await steam_skins_button(skins=result, query=message.text)
     )
     await state.clear()
     

     
@state_router.message(SkinPercentState.percent)
async def update_skin_percent(
     message: Message,
     state: FSMContext,
     session: Annotated[AsyncSession, Depend(async_db_session)],
     user: Annotated[User, Depend(get_user)],
     service: Annotated[StateService, Depend(get_state_service)]
):
     if message.text.isdigit() is False:
          return await message.answer("Процент должен быть число от 5 до 100.")
     
     percent = int(message.text)
     if percent < 5 or percent > 100:
          return await message.answer("Процент должен быть число от 5 до 100.")
     
     result = await service.update_skin_percent(
          session=session,
          user=user,
          percent=percent
     )
     await state.clear()
     return await message.answer(text=result.text)
     
     

@state_router.message(SteamIDState.steam_id)
async def steam_user(
     message: Message,
     state: FSMContext,
     service: Annotated[StateService, Depend(get_state_service)]
):
     if message.text.isdigit() is False:
          return await message.answer("ID должен быть числом!")
     
     result = await service.steam_user(steam_id=int(message.text))
     if isresponse(result):
          return await message.answer(result.text)

     await message.answer_photo(
          photo=URLInputFile(url=result.steam_avatar),
          caption=f"{result.steam_name} \n{link('Steam профиль', result.steam_profile_link)}",
          parse_mode=ParseMode.MARKDOWN,
          reply_markup=await steam_profile_button(
               steam_id=result.steam_id
          )
     )
     await state.clear()
     
     
     
     
      
          