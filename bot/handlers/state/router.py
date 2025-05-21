from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router


from bot.utils.inline import search_item_button
from bot.utils.filter.state import UpdateTimeState, SearchState, PercentState
from bot.schemas import UserDataclass, Time
from .service import StateService


state_router = Router(name="state_router")


@state_router.message(UpdateTimeState.time)
async def update_time(
     message: Message,
     state: FSMContext,
     user: UserDataclass,
     service: StateService
):
     valide_time = Time.from_str(message.text)
     if isinstance(valide_time, Time):
          await service.update_time(
               user=user,
               new_time=valide_time.to_string
          )
          await state.clear()
          return await message.answer(f"Время обновлено: {valide_time.pretty_string}")
     await message.answer(valide_time)
     
     
     
@state_router.message(SearchState.item)
async def search_item(
     message: Message,
     state: FSMContext,
     service: StateService
):
     result = await service.search_item(item=message.text)
     if isinstance(result, str):
          return await message.answer(result)
     
     await message.answer(
          text=f"Предметы по запросу: {message.text}",
          reply_markup=await search_item_button(items=result)
     )
     await state.clear()
     
   
     
@state_router.message(PercentState.percent)
async def update_create_percent(
     message: Message,
     state: FSMContext,
     user: UserDataclass,
     service: StateService
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
          await message.answer("Процент обновлён")
     await state.clear()
          