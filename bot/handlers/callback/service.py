from bot.utils.filter.callback import InventoryPaginateCallbackData
from bot.core.gen import generate_skin_id
from bot.http.steam import SteamHttpClient
from bot.db.repository import UserRepository, SkinRepository
from bot.schemas import UserDataclass



class CallbackService:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: SteamHttpClient
     ):
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          
          
     async def settings_notify(
          self,
          user: UserDataclass
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          await self.user_repository.update(
               where=user.where,
               values=update_data
          )
          return update_data.get("notify")
     
     
     async def delete_item(
          self,
          user: UserDataclass,
          item: str
     ) -> None:
          result = await self.skin_repository.delete(
               where={"owner": user.telegram_id, "name": item}
          )
          if result is False:
               return "Предмет в инвентаре не найден."
          return "Предмет успешно удалён."
          
     
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=SteamHttpClient()
     )