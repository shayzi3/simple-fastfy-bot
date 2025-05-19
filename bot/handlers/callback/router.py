from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.filter.callback import SkinNameCallbackData
from bot.utils.filter.state import UpdateTimeState
from bot.utils.inline import settings_button
from bot.schemas import UserDataclass
from .service import CallbackService



callback_router = Router(name="callback_router")



@callback_router.callback_query(F.data == "settings_notify")
async def settings_notify(
     query: CallbackQuery,
     user: UserDataclass,
     service: CallbackService
):
     result = await service.settings_notify(user=user)
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await settings_button(
               notify_status=result,
               update_time=user.update_time.pretty_string
          )
     )
     
     
@callback_router.callback_query(F.data == "settings_update_time")
async def settings_update_time(
     query: CallbackQuery,
     state: FSMContext
):
     await state.set_state(UpdateTimeState.time)
     await query.message.answer(
          (
               "Отправь дату в виде: day-hour-minute" +
               "\nПример: 0-0-25 Обновление будет происходить каждые 25 минут"
          )
     )
     
    
     
@callback_router.callback_query(SkinNameCallbackData.filter(F.mode == "skin"))
async def items(
     query: CallbackQuery,
     callback_data: SkinNameCallbackData,
     user: UserDataclass,
     service: CallbackService
):
     result = await service.items(
          user=user,
          item=callback_data.name
     )
     await query.answer(text=result)