from aiogram.filters.callback_data import CallbackData


class SkinCallbackData(CallbackData, prefix="+"):
     mode: str
     row: int
     index: int

     
class InventoryPaginateCallbackData(CallbackData, prefix="?"):
     mode: str
     index: int
     max_len: int
     