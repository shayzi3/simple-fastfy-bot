from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas.base import BaseSkinDataclass
from bot.utils.filter.callback import (
     InventoryPaginateCallbackData,
     SkinCallbackData,
)



async def settings_button(
     notify_status: bool,
     update_time: str
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     notify = "Enable"
     if notify_status is False:
          notify = "Disable"
     
     builder.add(
          InlineKeyboardButton(
               text=f"Уведомления: {notify}",
               callback_data="settings_notify"
          ),
          InlineKeyboardButton(
               text=f"Время обновления: {update_time}",
               callback_data="settings_update_time"
          )
     )
     builder.adjust(1, 1)
     return builder.as_markup()



async def search_item_button(
     items: list[str]
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     row = 0
     index = 0
     for num, name in enumerate(items):
          if (num % 2 == 0) and (num != 0):
               index = 0
               row += 1
               
          if (num % 2 != 0) and (num != 0):
               index += 1
          
          builder.add(
               InlineKeyboardButton(
                    text=name,
                    callback_data=SkinCallbackData(
                         mode="steam_skin",
                         row=row,
                         index=index
                    ).pack()
               )
          )
     builder.adjust(2)
     return builder.as_markup()


async def inventory_button_or_chart(
     skins: list[list[BaseSkinDataclass]],
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
     
     
     