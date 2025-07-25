from math import ceil

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas import SteamSkins
from bot.utils.filter.callback import Paginate, PaginateItem, SteamProfileCallback


async def settings_button(
     steam_tied: bool
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     text = "Сменить аккаунт" if steam_tied else "Привязать Steam"
     builder.add(
          InlineKeyboardButton(
               text=text,
               callback_data="settings_new_steam_account"
          ),
          InlineKeyboardButton(
               text="Изменить процент",
               callback_data="settings_update_skin_percent"
          )
     )
     builder.adjust(1, 1)
     return builder.as_markup()



async def steam_skins_button(
     skins: SteamSkins,
     offset: int = 0,
     current_page: int = 1,
     query: str = ""
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     offset_skins = skins.skins[offset:5 + offset]
     for skin_name in offset_skins:
          builder.add(
               InlineKeyboardButton(
                    text=skin_name,
                    callback_data=PaginateItem(
                         mode="steam_skin",
                         skin=skin_name # compress name
                    ).pack()
               )
          )
     builder.add(
          InlineKeyboardButton(
               text="<",
               callback_data=Paginate(
                    mode="steam_skin_paginate_left",
                    offset=offset,
                    all_pages=skins.pages,
                    current_page=current_page,
                    query=query
               ).pack()
          ),
          InlineKeyboardButton(
               text=f"{current_page}/{skins.pages}",
               callback_data="empty"
          ),
          InlineKeyboardButton(
               text=">",
               callback_data=Paginate(
                    mode="steam_skin_paginate_right",
                    offset=offset,
                    all_pages=skins.pages,
                    current_page=current_page,
                    query=query
               ).pack()
          )
     )
     builder.adjust(*[1 for _ in range(len(offset_skins))], 3)
     return builder.as_markup()
     


async def inventory_button(
     skins: list[str],
     offset: int = 0,
     current_page: int = 1
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     offset_skins = skins[offset:5 + offset]
     for skin_name in offset_skins:
          builder.add(
               InlineKeyboardButton(
                    text=skin_name,
                    callback_data=PaginateItem(
                         mode="inv_skin",
                         skin=skin_name
                    ).pack()
               )
          )
          
     pages = ceil(len(skins) / 5)
     builder.add(
          InlineKeyboardButton(
               text="<",
               callback_data=Paginate(
                    mode="inv_paginate_left",
                    offset=offset,
                    all_pages=pages,
                    current_page=current_page
               ).pack()
          ),
          InlineKeyboardButton(
               text=f"{current_page}/{pages}",
               callback_data="empty"
          ),
          InlineKeyboardButton(
               text=">",
               callback_data=Paginate(
                    mode="inv_paginate_right",
                    offset=offset,
                    all_pages=pages,
                    current_page=current_page
               ).pack()
          )
     )
     builder.adjust(*[1 for _ in range(len(offset_skins))], 3)
     return builder.as_markup()



async def inventory_item_button(
     compress_skin_name: str
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Удалить предмет",
               callback_data=PaginateItem(
                    mode="inv_skin_del",
                    skin=compress_skin_name
               ).pack()
          ),
          InlineKeyboardButton(
               text="График цены",
               callback_data=PaginateItem(
                    mode="inv_skin_graph",
                    skin=compress_skin_name
               ).pack()
          )
     )
     builder.adjust(1, 1)
     return builder.as_markup()
     


async def delete_button() -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Убрать сообщение",
               callback_data="delete_message"
          )
     )
     return builder.as_markup()


async def steam_profile_button(steamid: int) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Аккаунт мой",
               callback_data=SteamProfileCallback(steamid=steamid).pack()
          ),
          InlineKeyboardButton(
               text="Аккаунт не мой",
               callback_data="steam_account_not_valide"
          )
     )
     builder.adjust(1, 1)
     return builder.as_markup()
     
     
     
     