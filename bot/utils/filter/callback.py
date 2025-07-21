from aiogram.filters.callback_data import CallbackData

from bot.utils.compress import CompressSkinName


class Paginate(CallbackData, prefix="?"):
     mode: str
     offset: int
     all_pages: int
     current_page: int
     query: str = ""
     
     
     
class PaginateItem(CallbackData, prefix="-"):
     mode: str
     skin: str
     
     
     @property
     def skin_from_compress(self) -> str:
          return CompressSkinName.compress(
               name=self.skin,
               from_compress=True
          )
     
     
     
     
class SteamProfileCallback(CallbackData, prefix="="):
     steam_id: int     
     

     
     
     

     