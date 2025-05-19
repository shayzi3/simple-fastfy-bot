from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router


from bot.utils.inline import search_item_button
from bot.utils.filter.state import UpdateTimeState, SearchState
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
     await state.clear()
     if isinstance(result, str):
          return await message.answer(result)
     
     await message.answer(
          text=f"Предметы по запросу: {message.text}",
          reply_markup=await search_item_button(items=result)
     )