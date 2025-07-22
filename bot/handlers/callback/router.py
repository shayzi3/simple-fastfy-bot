from typing import Annotated

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_tool.depend import Depend
from aiogram_tool.limit import Limit
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.session import async_db_session
from bot.handlers.dependency import get_user, get_user_rel
from bot.responses import isresponse
from bot.utils.buttons.inline import (
    chart_buttons,
    inventory_button_or_chart,
    inventory_item_button,
    steam_skins_button,
)
from bot.utils.filter.callback import Paginate, PaginateItem, SteamProfileCallback
from bot.utils.filter.state import SkinPercentState, SteamIDState

from .service import CallbackService, get_callback_service

callback_router = Router(name="callback_router")



@callback_router.callback_query(F.data == "delete_message")
async def delete_message(query: CallbackQuery):
     await query.message.delete()
     


@callback_router.callback_query(
     F.data == "settings_update_skin_pecent", 
     Limit(seconds=5)
)
async def setting_update_skin_percent(
     query: CallbackQuery,
     state: FSMContext
):
     await state.set_state(SkinPercentState.percent)
     await query.message.answer("Отправь число от 5 до 100")
     await query.answer()

     
     
     
@callback_router.callback_query(
     F.data.in_(["settings_new_steam_account", "steam_account_not_valide"]), 
     Limit(minutes=2)
)
async def settings_new_steam_account(
     query: CallbackQuery,
     state: FSMContext
):
     await state.set_state(SteamIDState.steam_id)
     await query.message.answer("Отправь мне SteamID")
     await query.answer()
     
     
     
@callback_router.callback_query(
     SteamProfileCallback.filter(),
     Limit(minutes=2)
)
async def register_new_steam_account(
     query: CallbackQuery,
     callback_data: SteamProfileCallback,
     session: Annotated[AsyncSession, Depend(async_db_session)],
     user: Annotated[User, Depend(get_user)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     if user.steam_id == callback_data.steam_id:
          return await query.answer("Этот аккаунт уже привязан.")
     
     result = await service.register_new_steam_account(
          session=session,
          user=user,
          steam_id=callback_data.steam_id
     )
     await query.answer(text=result.text)
     
    
    
@callback_router.callback_query(
     PaginateItem.filter(F.mode == "steam_skin"),
     Limit(seconds=3)
)
async def steam_skin(
     query: CallbackQuery,
     callback_data: PaginateItem,
     user: Annotated[User, Depend(get_user_rel)],
     session: Annotated[AsyncSession, Depend(async_db_session)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     for user_skin in user.skins:
          if user_skin.skin_name == callback_data.skin_from_compress:
               return await query.answer("Такой скин уже есть в инвентаре!")
     
     result = await service.steam_skin(
          session=session,
          user=user,
          skin_hash_name=callback_data.skin_from_compress
     )
     await query.answer(text=result.text.format(callback_data.skin_from_compress))
     
     
     
@callback_router.callback_query(
     Paginate.filter(F.data.contains("steam_skin_paginate")),
     Limit(seconds=5)
)
async def steam_skin_paginate(
     query: CallbackQuery,
     callback_data: Paginate,
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     if (
          (callback_data.current_page == 1)
          or (callback_data.current_page == callback_data.all_pages)
     ):
          return await query.answer("Дальше листать не получится")
     
     result = await service.steam_skin_paginate(
          callback_data=callback_data.model_copy()
     )
     if isresponse(result):
          return await query.answer(text=result.text)
     
     skins, data = result
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await steam_skins_button(
               skins=skins,
               offset=data.offset,
               current_page=data.current_page,
               query=data.query
          )
     )
     
     
     
     
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
     
     