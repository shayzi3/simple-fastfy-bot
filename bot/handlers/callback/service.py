import os

from bot.core.timezone import time_now
from bot.db.json_storage import JsonStorage
from bot.db.repository import SkinRepository, UserRepository
from bot.http.steam import SteamHttpClient
from bot.schemas import UserDataclass
from bot.utils.chart import Chart


class CallbackService:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: SteamHttpClient,
          json_storage: JsonStorage,
          chart: Chart
     ):
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          self.json_storage = json_storage
          self.chart = chart
          
          
     async def settings_notify(
          self,
          user: UserDataclass
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          if update_data.get("notify") is True:
               await self.json_storage.add(
                    new_value = (
                         f"{user.update_time.to_string};"
                         f"{(time_now() + user.update_time.to_timedelta()).isoformat()};"
                         f"{user.telegram_id}"
                    )
               )
          else:
               await self.json_storage.delete(search_string=f"{user.telegram_id}")
          
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
          await self.skin_repository.delete(
               where={"owner": user.telegram_id, "name": item}
          )          
          
          
     async def chart_item(
          self,
          name: str,
          prices: list[int],
          telegram_id: int
     ) -> str:
          return await self.chart.chart_generate(
               prices=prices,
               filename=f"{telegram_id}.png",
               name=name
          )
          
          
     async def delete_chart_file(
          self,
          path: str
     ) -> None:
          if os.path.exists(path) is True:
               os.remove(path)   
               
               
     async def reset_chart(
          self,
          user: UserDataclass,
          skin_name: str
     ) -> str | None:
          item_price = await self.http_client.item_price(item=skin_name)
          if isinstance(item_price, float) is False:
               return "Повторите попытку позже"
          
          await self.skin_repository.update(
               where={"owner": user.telegram_id, "name": skin_name},
               values={"price_chart": f"{item_price},"}
          )
          
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=SteamHttpClient(),
          json_storage=JsonStorage(),
          chart=Chart()
     )