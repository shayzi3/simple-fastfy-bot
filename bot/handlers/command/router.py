from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.utils.filter.state import SearchState
from bot.utils.inline import settings_button, inventory_button
from bot.schemas import UserDataclass
from .service import CommandService


command_router = Router(name="command_router")


@command_router.message(CommandStart())
async def start(
     message: Message,
     user: UserDataclass,
     service: CommandService
):
     if user is None:
          await service.start(telegram_id=message.from_user.id)
     await message.answer("Я - бот, который поможет тебе отслеживать цены предметов CS2.")
     
     

@command_router.message(Command("settings"))
async def settings(
     message: Message,
     user: UserDataclass
):
     await message.answer(
          text="Настройки",
          reply_markup=await settings_button(
               notify_status=user.notify,
               update_time=user.update_time.pretty_string
          )
     )
     
     
   
@command_router.message(Command("clear"))
async def clear(
     message: Message,
     state: FSMContext
):
     get_state = await state.get_state()
     if get_state is not None:
          await state.clear()
          return await message.answer("Событие пропущено.")
     return await message.answer("Событий не найдено.")



@command_router.message(Command("search"))
async def search(
     message: Message,
     state: FSMContext
):
     await state.set_state(SearchState.item)
     await message.answer("Отправь название скина")
     
    
     
@command_router.message(Command("inventory"))
async def inventory(
     message: Message,
     user: UserDataclass,
):
     if not user.skins:
          return await message.answer("Ваш инвентарь пуст.")
     
     await message.answer(
          text="Инвентарь",
          reply_markup=await inventory_button(
               skins=user.sorted_skin_by_6(),
               index=0
          )
     )