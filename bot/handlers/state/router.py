from typing import Annotated

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from aiogram.utils.markdown import link

from bot.db.repository import get_user
from bot.schemas import UserModel
from bot.utils.depend import Depend
from bot.utils.filter.state import PercentState, SearchState, SteamIDState
from bot.utils.inline import search_item_button, steam_profile_button
from bot.utils.responses import isresponse

from .service import StateService, get_state_service

state_router = Router(name="state_router")

     
     
@state_router.message(SearchState.item)
async def search_item(
     message: Message,
     state: FSMContext,
     service: Annotated[StateService, Depend(get_state_service)]
):
     result = await service.search_item(item=message.text)
     if isresponse(result):
          return await message.answer(result.text)
     
     await message.answer(
          text=f"Предметы по запросу: {message.text}",
          reply_markup=await search_item_button(items=result)
     )
     await state.clear()
     

     
@state_router.message(PercentState.percent)
async def update_create_percent(
     message: Message,
     state: FSMContext,
     user: Annotated[UserModel, Depend(get_user)],
     service: Annotated[StateService, Depend(get_state_service)]
):
     if message.text.isdigit() is False:
          return await message.answer("Процент должен быть число от 3 до 90")
     
     if int(message.text) < 3 or int(message.text) > 90:
          return await message.answer("Процент должен быть число от 3 до 90")
     
     data = await state.get_data()
     if data.get("mode") == "create":
          result = await service.create_item_with_percent(
               item=data.get("skin_name"),
               user=user,
               percent=int(message.text)
          )
          await message.answer(result)
          
     if data.get("mode") == "update":
          result = await service.update_item_percent(
               user=user,
               item=data.get("skin_name"),
               percent=int(message.text)
          )
          await message.answer(f"Процент для скина {data.get('skin_name')} обновлён")
     await state.clear()
     
     

@state_router.message(SteamIDState.steamid)
async def steam_user(
     message: Message,
     state: FSMContext,
     service: Annotated[StateService, Depend(get_state_service)]
):
     steamid_ = message.text
     if steamid_.isdigit() is False:
          return await message.answer("ID должен быть числом!")
     
     result = await service.steam_user(steamid=int(message.text))
     if isresponse(result):
          return await message.answer(result.text)
     
     await message.answer_photo(
          photo=URLInputFile(url=result.avatarmedium),
          caption=f"{result.personaname} \n{link('Steam профиль', result.profileurl)}",
          parse_mode=ParseMode.MARKDOWN,
          reply_markup=await steam_profile_button(
               steamid=int(message.text)
          )
     )
     await state.clear()
     
     
     
      
          