from aiogram.filters.callback_data import CallbackData



class SkinNameCallbackData(CallbackData, prefix="?"):
     mode: str
     name: str
     
     
class InventoryPaginateCallbackData(CallbackData, prefix="?"):
     mode: str
     index: int
     max_len: int
     