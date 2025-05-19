from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.schemas.base import BaseSkinDataclass
from bot.utils.filter.callback import (
     SkinNameCallbackData,
     InventoryPaginateCallbackData
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
     
     for name in items:
          builder.add(
               InlineKeyboardButton(
                    text=name,
                    callback_data=SkinNameCallbackData(name=name, mode="skin_steam").pack()
               )
          )
     builder.adjust(2)
     return builder.as_markup()


async def inventory_button(
     skins: list[list[BaseSkinDataclass]],
     index: int
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     try:
          skins_by_index = skins[index]
     except IndexError:
          skins_by_index = skins[0]
          
     for skin in skins_by_index:
          builder.add(
               InlineKeyboardButton(
                    text=skin.name,
                    callback_data=SkinNameCallbackData(name=skin.name, mode="skin_inv").pack()
               )
          )
          
     builder.add(
          InlineKeyboardButton(
               text="<",
               callback_data=InventoryPaginateCallbackData(
                    mode="inventory_left",
                    index=index,
                    max_len=len(skins) - 1
               ).pack()
          ),
          InlineKeyboardButton(
               text=">",
               callback_data=InventoryPaginateCallbackData(
                    mode="inventory_right",
                    index=index,
                    max_len=len(skins) - 1
               ).pack()
          )
     )
     builder.adjust(2)
     return builder.as_markup()
     
     
     
     