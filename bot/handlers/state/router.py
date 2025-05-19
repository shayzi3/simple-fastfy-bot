from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router


from bot.utils.filter.state import UpdateTime
from bot.schemas import UserDataclass, Time
from .service import StateService


state_router = Router(name="state_router")


@state_router.message(UpdateTime.time)
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
     