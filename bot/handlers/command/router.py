from typing import Annotated

from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.db.repository import get_user
from bot.schemas import UserModel
from bot.utils.depend import Depend
from bot.utils.filter.state import SearchState, SteamIDState
from bot.utils.filter.timeout import RateLimit
from bot.utils.inline import inventory_button_or_chart, settings_button

command_router = Router(name="command_router")



@command_router.message(CommandStart())
async def start(message: Message):
     await message.answer(
          "Я - бот, который поможет тебе отслеживать цены предметов CS2. Пропиши команду /help"
     )
     
     

@command_router.message(Command("settings"), RateLimit(seconds=1))
async def settings(
     message: Message,
     user: Annotated[UserModel, Depend(get_user)]
):
     await message.answer(
          text="Настройки",
          reply_markup=await settings_button(
               notify_status=user.notify
          )
     )
     
     
   
@command_router.message(Command("skip"))
async def clear(
     message: Message,
     state: FSMContext
):
     get_state = await state.get_state()
     if get_state is not None:
          await state.clear()
          return await message.answer("Событие пропущено")
     return await message.answer("Событий не найдено")



@command_router.message(Command("search"), RateLimit(seconds=5))
async def search(
     message: Message,
     state: FSMContext
):
     await state.set_state(SearchState.item)
     await message.answer("Отправь название скина")
     
    
     
@command_router.message(Command("inventory"), RateLimit(seconds=2))
async def inventory(
     message: Message,
     user: Annotated[UserModel, Depend(get_user)],
):
     if not user.skins:
          return await message.answer("Ваш инвентарь пуст")
     
     await message.answer(
          text="Инвентарь",
          reply_markup=await inventory_button_or_chart(
               skins=user.sorted_skin_by_6(),
               index=0,
               mode="inventory_item"
          )
     )
     
     
@command_router.message(Command("help"))
async def help(message: Message):
     bot_description = "🤖 Бот для отслеживания цен на скины"

     functions = [
          "🔍 <b>Добавление предмета в инвентарь</b>\nИспользуйте команду /search, чтобы добавить предмет для отслеживания.",
          "📊 <b>Установка процента отклонения цены</b>\nУкажите процент для каждого предмета. Если цена изменится на указанный процент в большую или меньшую сторону, вы получите уведомление.",
          "🔔 <b>Включение уведомлений</b>\nПереключите статус уведомлений на `Enabled`, чтобы получать оповещения об изменении стоимости.",
          "⏰ <b>Изменение времени обновления</b>\nУстановите интервал обновления в формате days-hours-minutes. Например, 0-0-35 означает, что бот будет проверять стоимость предметов каждые 35 минут."
     ]

     msg = f"{bot_description}\n\n" + "\n\n".join(functions)
     await message.answer(text=msg, parse_mode=ParseMode.HTML)
     
     
     
@command_router.message(Command("chart"), RateLimit(seconds=10))
async def chart(
     message: Message,
     user: Annotated[UserModel, Depend(get_user)]
):
     if not user.skins:
          return await message.answer("Ваш инвентарь пуст")
     
     await message.answer(
          text="Инвентарь",
          reply_markup=await inventory_button_or_chart(
               skins=user.sorted_skin_by_6(),
               index=0,
               mode="chart_item"
          )
     )
     
     
     
@command_router.message(Command("steam"), RateLimit(seconds=2))
async def steam(
     message: Message,
     state: FSMContext
):
     await state.set_state(SteamIDState.steamid)
     await message.answer("Отправь свой SteamID")