from math import ceil
from typing import Annotated

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_tool.depend import Depend
from aiogram_tool.limit import Limit
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.session import async_db_session
from bot.handlers.dependency import get_user, get_user_rel
from bot.responses import isresponse
from bot.utils.buttons.inline import (
    inventory_button,
    inventory_item_button,
    steam_skins_button,
)
from bot.utils.compress import CompressSkinName
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
     if any(
          [skin.skin_name == callback_data.skin_from_compress for skin in user.skins]
     ) is True:
          return await query.answer("Такой скин уже есть в инвентаре!")
     
     result = await service.steam_skin(
          session=session,
          user=user,
          skin_hash_name=callback_data.skin_from_compress
     )
     await query.answer(text=result.text.format(callback_data.skin_from_compress))
     
     
     
@callback_router.callback_query(
     Paginate.filter(F.data.contains("steam_skin_paginate")),
     Limit(seconds=3)
)
async def steam_paginate(
     query: CallbackQuery,
     callback_data: Paginate,
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     if (
          ((callback_data.current_page == 1) and ("left" in callback_data.mode))
          or 
          ((callback_data.current_page == callback_data.all_pages) and ("right" in callback_data.mode))
     ):
          return await query.answer("Дальше листать не получится!")
     
     result = await service.steam_paginate(
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
     
    
    
@callback_router.callback_query(
     PaginateItem.filter(F.data == "inv_skin"),
     Limit(seconds=3)
) 
async def inventory_skin(
     query: CallbackQuery,
     callback_data: PaginateItem,
     user: Annotated[User, Depend(get_user_rel)],
):
     if any(
          [skin.skin_name == callback_data.skin_from_compress for skin in user.skins]
     ) is False:
          return await query.answer("Такого предмета нет в инвентаре")
     
     current_skin = next(
          (skin for skin in user.skins if skin.skin_name == callback_data.skin_from_compress)
     )
     await query.message.answer(
          text=current_skin.skin_info(),
          reply_markup=await inventory_item_button(
               compress_skin_name=callback_data.skin
          ),
          parse_mode=ParseMode.MARKDOWN_V2
     )
     
     
@callback_router.callback_query(
     Paginate.filter(F.mode.contains("inv_paginate")),
     Limit(seconds=3)
)
async def inventory_paginate(
     query: CallbackQuery,
     callback_data: Paginate,
     user: Annotated[User, Depend(get_user_rel)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     if not user.skins:
          return await query.answer("Ваш инвентарь пуст")
     
     if callback_data.all_pages == ceil(len(user.skins) / 5):
          if (
               ((callback_data.current_page == 1) and ("left" in callback_data.mode))
               or 
               ((callback_data.current_page == callback_data.all_pages) and ("right" in callback_data.mode))
          ):
               return await query.answer("Дальше листать не получится!")
     
     result = await service.inventory_paginate(
          callback_data=callback_data.model_copy(),
          user_skins=user.skins
     )
     await query.message.edit_reply_markup(
          inline_message_id=query.inline_message_id,
          reply_markup=await inventory_button(
               skins=[
                    CompressSkinName.compress(
                         name=skin.skin_name,
                         from_compress=False
                    ) for skin in user.skins
               ],
               offset=result.offset,
               current_page=result.current_page
          )
     )
     
     
     
@callback_router.callback_query(
     PaginateItem.filter(F.data == "inv_skin_del"),
     Limit(seconds=3)
)
async def inventory_skin_delete(
     query: CallbackQuery,
     callback_data: PaginateItem,
     user: Annotated[User, Depend(get_user_rel)],
     session: Annotated[AsyncSession, Depend(async_db_session)],
     service: Annotated[CallbackService, Depend(get_callback_service)]
):
     result = await service.inventory_skin_delete(
          session=session,
          user=user,
          skin_name=callback_data.skin_from_compress
     )
     text = result.text
     if getattr(result, "__name__", "") == "SkinDelete":
          text = result.text.format(callback_data.skin_from_compress)
     await query.answer(text=text)
     
     
     
@callback_router.callback_query(
     PaginateItem.filter(F.data == "inv_skin_graph")
)
async def inventory_skin_delete(
     query: CallbackQuery,
     callback_data: PaginateItem
):
     ...
     
     
     
     

     
     