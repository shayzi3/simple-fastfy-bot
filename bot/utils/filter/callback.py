from aiogram.filters.callback_data import CallbackData


class Mode(CallbackData, prefix="?"):
     mode: str



class SkinCallbackData(Mode, prefix="+"):
     row: int
     index: int
     
     
class InventoryPaginateCallbackData(Mode, prefix="="):
     button_mode: str
     index: int
     max_len: int
     
     
     
class SteamProfileCallback(Mode, prefix="-"):
     steamid: int
     
     
     

     