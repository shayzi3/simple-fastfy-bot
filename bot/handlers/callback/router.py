from typing import Annotated

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from bot.db.repository import get_user
from bot.schemas import UserModel
from bot.utils.depend import Depend
from bot.utils.filter.callback import (
    InventoryPaginateCallbackData,
    SkinCallbackData,
    SteamProfileCallback,
)
from bot.utils.filter.state import PercentState, SteamIDState
from bot.utils.inline import (
    chart_buttons,
    inventory_button_or_chart,
    inventory_item_button,
    settings_button,
)
from bot.utils.responses import isresponse

from .service import CallbackService, get_callback_service

callback_router = Router(name="callback_router")



@callback_router.callback_query(F.data == "delete_message")
async def delete_message(query: CallbackQuery):
     await query.message.delete()
     


@callback_router.callback_query(F.data == "settings_notify")
async def settings_notify(
     query: CallbackQuery,
     user: Annotated[UserModel, Depend(get_user)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     result = await service.settings_notify(user=user)
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await settings_button(
               notify_status=result,
          )
     )
     
    
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "steam_skin"))
async def steam_item(
     query: CallbackQuery,
     state: FSMContext,
     callback_data: SkinCallbackData,
     user: Annotated[UserModel, Depend(get_user)]
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     
     if len(user.skins) >= 30:
          return await query.answer("Максимальное кол-во предметов в инвентаре 30!")
     
     if user.get_skin(name) is not None:
          return await query.answer(f"Предмет {name} уже есть в инвентаре.")
          
     await state.set_data({"skin_name": name, "mode": "create"})
     await state.set_state(PercentState.percent)
     await query.message.answer("Отправь процент")
     await query.answer()
     
     
     
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "inventory_item"))
async def inventory_item(
     query: CallbackQuery,
     user: Annotated[UserModel, Depend(get_user)],
     callback_data: SkinCallbackData
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     
     skin = user.get_skin(name)
     if skin is None:
          return await query.answer(f"Предмет {name} не найден в инвенторе")
     
     await query.message.answer(
          text=f"{name} \nПроцент: {skin.percent}",
          reply_markup=await inventory_item_button()
     )
     await query.answer()
     
     
     
@callback_router.callback_query(SkinCallbackData.filter(F.mode == "chart_item"))
async def chart_item(
     query: CallbackQuery,
     callback_data: SkinCallbackData,
     user: Annotated[UserModel, Depend(get_user)],
     service: CallbackService
):
     keyboard = query.message.reply_markup.inline_keyboard
     name = keyboard[callback_data.row][callback_data.index].text
     
     message = await query.message.answer("Идёт генерация графика...")
     
     skin = user.get_skin(name)
     if skin is None:
          return await query.answer(f"Предмет {name} не найден в инвенторе")
     
     chart = await service.chart_item(
          name=name,
          prices=skin.price_chart,
          telegram_id=query.from_user.id
     )
     await message.delete()
     await query.message.answer_photo(
          caption=name,
          photo=FSInputFile(path=chart),
          reply_markup=await chart_buttons()
     )
     await service.delete_chart_file(chart)
     await query.answer()
     
     
     
@callback_router.callback_query(
     InventoryPaginateCallbackData.filter(F.mode == "inventory_left")
)
async def inventory_left(
     query: CallbackQuery,
     callback_data: InventoryPaginateCallbackData,
     user: Annotated[UserModel, Depend(get_user)]
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
     user: Annotated[UserModel, Depend(get_user)]
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
     user: Annotated[UserModel, Depend(get_user)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     name = query.message.text.split("\n")[0].strip()
     if user.get_skin(name) is None:
          return await query.answer(f"Предмет {name} не найден в инвенторе")
     
     await service.delete_item(
          user=user,
          item=name
     )
     await query.answer(f"Предмет {name} успешно удалён")
     await query.message.delete()
     
     
  
@callback_router.callback_query(F.data == "create_skin_or_update_percent")
async def create_skin_or_update_percent(
     query: CallbackQuery,
     user: Annotated[UserModel, Depend(get_user)],
     state: FSMContext
):
     name = query.message.text.split("\n")[0].strip()
     if user.get_skin(name) is None:
          return await query.answer(f"Предмет {name} не найден в инвенторе")
     
     await state.set_state(PercentState.percent)
     await state.set_data({"skin_name": name, "mode": "update"})
     await query.message.answer("Отправь процент")
     await query.answer()
     


@callback_router.callback_query(F.data == "reset_chart")
async def reset_chart(
     query: CallbackQuery,
     user: Annotated[UserModel, Depend(get_user)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     name = query.message.caption.strip()
     if name in user.skins_names:
          return await query.answer(f"Предмет {name} не найден в инвентаре")
     
     result = await service.reset_chart(user=user, skin_name=name)
     if isresponse(result):
          return await query.message.answer(result.text)
     
     await query.message.delete()
     await query.message.answer(f"График для скина {name} сброшен")
     
     
     
@callback_router.callback_query(F.data == "steam_account_not_valide")
async def steam_account_not_valide(
     query: CallbackQuery,
     state: FSMContext
):
     await query.answer()
     await query.message.answer("Отправь другой SteamID")
     await state.set_state(SteamIDState.steamid)
     
     
     
@callback_router.callback_query(SteamProfileCallback.filter(F.mode == "steam_profile"))
async def steam_profile(
     query: CallbackQuery,
     callback_data: SteamProfileCallback,
     user: Annotated[UserModel, Depend(get_user)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     msg = await query.message.answer(
          "Начинаю выгрузку предметов. Это может занять некоторое время."
     )
     await query.answer()
     
     result = await service.steam_inventory(
          user=user,
          steamid=callback_data.steamid
     )
     if isresponse(result):
          await msg.delete()
          return await query.message.answer(result.text)
     
     text = "*Добавленные предметы*\n"
     text += "\n\n".join(result)

     await msg.delete()
     await query.message.answer(
          text=text,
          parse_mode=ParseMode.MARKDOWN
     )
     
     
     
     