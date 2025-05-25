from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.utils.filter.callback import (
     InventoryPaginateCallbackData,
     SkinCallbackData
)
from bot.utils.filter.state import UpdateTimeState, PercentState
from bot.utils.inline import (
     settings_button, 
     inventory_button_or_chart, 
     inventory_item_button,
     delete_button
)
from bot.schemas import UserDataclass
from .service import CallbackService



callback_router = Router(name="callback_router")



@callback_router.callback_query(F.data == "delete_message")
async def delete_message(query: CallbackQuery):
     await query.message.delete()
     


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
               "Отправь дату в виде: day-hour-minute"
               "\nПример: 0-0-25." 
               "\nОбновление будет происходить каждые 25 минут"
          )
     )
     await query.answer()
     
    
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "steam_skin"))
async def steam_item(
     query: CallbackQuery,
     state: FSMContext,
     callback_data: SkinCallbackData,
     user: UserDataclass
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     if len(user.skins) >= 30:
          return await query.answer("Максимальное кол-во предметов в инвентаре 20!")
     
     if user.get_skin(name) is not None:
          return await query.answer("Такой предмет уже есть в инвентаре.")
          
     await state.set_data({"skin_name": name, "mode": "create"})
     await state.set_state(PercentState.percent)
     await query.message.answer("Отправь процент")
     await query.answer()
     
     
     
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "inventory_item"))
async def inventory_item(
     query: CallbackQuery,
     user: UserDataclass,
     callback_data: SkinCallbackData
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     skin = user.get_skin(name)
     if skin is None:
          return await query.answer("Предмет в инвентаре не найден")
     
     await query.message.answer(
          text=f"{name} \nПроцент: {skin.percent}",
          reply_markup=await inventory_item_button()
     )
     await query.answer()
     
     
     
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "chart_item"))
async def chart_item(
     query: CallbackQuery,
     callback_data: SkinCallbackData,
     user: UserDataclass,
     service: CallbackService
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     
     message = await query.message.answer("Идёт генерация графика...")
     
     skin = user.get_skin(name)
     if skin is None:
          return await query.answer("Предмет в инвентаре не найден")
     
     chart = await service.chart_item(
          name=name,
          prices=skin.price_chart,
          telegram_id=query.from_user.id
     )
     await message.delete()
     await query.message.answer_photo(
          caption=name,
          photo=FSInputFile(path=chart),
          reply_markup=await delete_button()
     )
     await service.delete_chart_file(chart)
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
          return await query.answer("Ваш инвентарь пуст")
     
     if callback_data.index <= 0:
          return await query.answer("Дальше листать не получится")
     
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await inventory_button_or_chart(
               skins=user.sorted_skin_by_6(),
               index=callback_data.index - 1,
               mode=callback_data.button_mode
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
          return await query.answer("Ваш инвентарь пуст")
     
     if callback_data.index >= callback_data.max_len:
          return await query.answer("Дальше листать не получится")
     
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await inventory_button_or_chart(
               skins=user.sorted_skin_by_6(),
               index=callback_data.index + 1,
               mode=callback_data.button_mode
          )
     )
     
     
@callback_router.callback_query(F.data == "delete_item")
async def delete_item(
     query: CallbackQuery,
     user: UserDataclass,
     service: CallbackService
):
     name = query.message.text.split("\n")[0].strip()
     if user.get_skin(name) is None:
          return await query.answer("Предмет в инвентаре не найден")
     
     await service.delete_item(
          user=user,
          item=name
     )
     await query.answer("Предмет успешно удалён")
     await query.message.delete()
     
     
     
@callback_router.callback_query(F.data == "create_skin_or_update_percent")
async def create_skin_or_update_percent(
     query: CallbackQuery,
     user: UserDataclass,
     state: FSMContext
):
     name = query.message.text.split("\n")[0].strip()
     if user.get_skin(name) is None:
          return await query.answer("Предмет в инвентаре не найден")
     
     await state.set_state(PercentState.percent)
     await state.set_data({"skin_name": name, "mode": "update"})
     await query.message.answer("Отправь процент")
     await query.answer()
     