from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.filter.callback import SkinNameCallbackData



async def settings_button(
     notify_status: bool,
     update_time: str
) -> InlineKeyboardMarkup:
     builder = InlineKeyboardBuilder()
     
     notify = "Onn"
     if notify_status is False:
          notify = "Off"
     
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
                    callback_data=SkinNameCallbackData(name=name, mode="skin").pack()
               )
          )
     builder.adjust(2)
     return builder.as_markup()
     
     
     