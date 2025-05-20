from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.utils.filter.callback import (
     SkinNameCallbackData, 
     InventoryPaginateCallbackData
)
from bot.utils.filter.state import UpdateTimeState, PercentState
from bot.utils.inline import settings_button, inventory_button, inventory_item_button
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
     
    
@callback_router.callback_query(SkinNameCallbackData.filter(F.mode == "skin_steam"))
async def steam_item(
     query: CallbackQuery,
     callback_data: SkinNameCallbackData,
     state: FSMContext,
     user: UserDataclass
):
     if len(user.skins) >= 20:
          return await query.answer("Максимальное кол-во предметов в инвентаре 20!")
     
     skin = user.get_skin(callback_data.name)
     if skin:
          return await query.answer("Такой предмет уже есть в инвентаре.")
          
     await state.set_data({"skin_name": callback_data.name, "mode": "create"})
     await state.set_state(PercentState.percent)
     await query.message.answer("Отправь число процента.")
     await query.answer()
     
     
     
@callback_router.callback_query(SkinNameCallbackData.filter(F.mode == "skin_inv"))
async def inventory_item(
     query: CallbackQuery,
     user: UserDataclass,
     callback_data: SkinNameCallbackData,
):
     skin = user.get_skin(callback_data.name)
     if skin is None:
          return await query.answer("Предмет в инвентаре не найден.")
     
     await query.message.answer(
          text=f"{callback_data.name} \nПроцент: {skin.percent}",
          reply_markup=await inventory_item_button(
               item=callback_data.name
          )
     )
     await query.answer()
     
     
@callback_router.callback_query(
     InventoryPaginateCallbackData.filter(F.mode == "inventory_left")
)
async def inventory_left(
     query: CallbackQuery,
     callback_data: InventoryPaginateCallbackData,
     user: UserDataclass
):
     if not user.skins:
          return await query.answer("Ваш инвентарь пуст.")
     
     if callback_data.index <= 0:
          return await query.answer("Дальше листать не получится.")
     
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await inventory_button(
               skins=user.sorted_skin_by_6(),
               index=callback_data.index - 1
          )
     )
     
 
@callback_router.callback_query(
     InventoryPaginateCallbackData.filter(F.mode == "inventory_right")
)
async def inventory_right(
     query: CallbackQuery,
     callback_data: InventoryPaginateCallbackData,
     user: UserDataclass
):
     if not user.skins:
          return await query.answer("Ваш инвентарь пуст.")
     
     if callback_data.index >= callback_data.max_len:
          return await query.answer("Дальше листать не получится.")
     
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await inventory_button(
               skins=user.sorted_skin_by_6(),
               index=callback_data.index + 1
          )
     )
     
     
@callback_router.callback_query(
     SkinNameCallbackData.filter(F.mode == "del_item")
)
async def delete_item(
     query: CallbackQuery,
     callback_data: SkinNameCallbackData,
     user: UserDataclass,
     service: CallbackService
):
     result = await service.delete_item(
          user=user,
          item=callback_data.name
     )
     await query.answer(result)
     
     
     
@callback_router.callback_query(
     SkinNameCallbackData.filter(F.mode == "up_percent")
)
async def update_percent(
     query: CallbackQuery,
     callback_data: SkinNameCallbackData,
     user: UserDataclass,
     state: FSMContext
):
     skin = user.get_skin(callback_data.name)
     if skin is None:
          return await query.answer("Предмет в инвентаре не найден.")
     
     await state.set_state(PercentState.percent)
     await state.set_data({"skin_name": callback_data.name, "mode": "update"})
     await query.message.answer("Отправь число процента.")
     await query.answer()
     