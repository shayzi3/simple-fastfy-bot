from datetime import datetime
from bot.http.steam import SteamHttpClient
from bot.db.repository import UserRepository, SkinRepository
from bot.schemas import UserDataclass
from bot.schemas import Time
from bot.db.json_storage import JsonStorage



class CallbackService:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: SteamHttpClient,
          json_storage: JsonStorage
     ):
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          self.json_storage = json_storage
          
          
     async def settings_notify(
          self,
          user: UserDataclass
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          if update_data.get("notify") is True:
               await self.worker_json.add(
                    new_value = (
                         f"{user.update_time.to_string};"
                         f"{(datetime.now() + Time.from_str(user.update_time.to_string).to_timedelta()).isoformat()};"
                         f"{user.telegram_id}"
                    )
               )
               
          else:
               await self.worker_json.delete(search_string=f"{user.telegram_id}")
          
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
          http_client=SteamHttpClient(),
          json_storage=JsonStorage()
     )