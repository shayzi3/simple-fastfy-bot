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
          )
     )
     builder.add(
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
     for skin_name in skins.skins[offset:5 + offset]:
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
          )
     )
     builder.add(
          InlineKeyboardButton(
               text=f"{current_page}/{skins.pages}"
          )
     )
     builder.add(
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
     builder.adjust(1, 1, 1, 1, 1, 3)
     return builder.as_markup()
     


async def inventory_button_or_chart(
     skins: list[list],
     index: int,
     mode: str
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     try:
          skins_by_index = skins[index]
     except IndexError:
          skins_by_index = skins[0]
          
     row = 0
     index_ = 0
     for num, skin in enumerate(skins_by_index):
          if (num % 2 == 0) and (num != 0):
               index_ = 0
               row += 1
               
          if (num % 2 != 0) and (num != 0):
               index_ += 1
               
          builder.add(
               InlineKeyboardButton(
                    text=skin.name,
                    callback_data=SkinCallbackData(
                         mode=mode,
                         row=row,
                         index=index_
                    ).pack()
               )
          )
          
     builder.add(
          InlineKeyboardButton(
               text="<",
               callback_data=InventoryPaginateCallbackData(
                    mode="inventory_left",
                    index=index,
                    max_len=len(skins) - 1,
                    button_mode=mode
               ).pack()
          ),
          InlineKeyboardButton(
               text=">",
               callback_data=InventoryPaginateCallbackData(
                    mode="inventory_right",
                    index=index,
                    max_len=len(skins) - 1,
                    button_mode=mode
               ).pack()
          )
     )
     builder.adjust(2)
     return builder.as_markup()



async def inventory_item_button() -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Удалить предмет",
               callback_data="delete_item"
          ),
          InlineKeyboardButton(
               text="Изменить процент",
               callback_data="create_skin_or_update_percent",
          ),
          InlineKeyboardButton(
               text="Убрать сообщение",
               callback_data="delete_message"
          )
     )
     builder.adjust(1)
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



async def chart_buttons() -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     builder.add(
          InlineKeyboardButton(
               text="Сбросить график",
               callback_data="reset_chart"
          ),
          InlineKeyboardButton(
               text="Убрать сообщение",
               callback_data="delete_message"
          )
     )
     builder.adjust(1, 1)
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
     
     
     
     