import asyncio
import os

from bot.core.gen import generate_skin_id
from bot.core.timezone import time_now
from bot.db.json_storage import JsonStorage
from bot.db.repository import SkinRepository, UserRepository
from bot.infrastracture.http.steam import SteamHttpClient
from bot.schemas import UserModel
from bot.utils.chart import Chart
from bot.utils.responses import AnyResponse, InventoryLimit, TryLater, isresponse


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
          user: UserModel
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          await self.user_repository.update(
               where=user.where,
               values=update_data,
               delete_redis_value=user.delete_redis_values
          )
          return update_data.get("notify")
     
     
     async def delete_item(
          self,
          user: UserModel,
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
          user: UserModel,
          skin_name: str
     ) -> AnyResponse | None:
          item_price = await self.http_client.item_price(item=skin_name)
          if isinstance(item_price, float) is False:
               return TryLater
          
          await self.skin_repository.update(
               where={"owner": user.telegram_id, "name": skin_name},
               values={"price_chart": f"{item_price},"}
          )
          
     async def steam_inventory(
          self,
          user: UserModel,
          steamid: int
     ) -> AnyResponse | list[str]:
          if len(user.skins) >= 30:
               return InventoryLimit
          
          steam_inventory = await self.http_client.inventory_by_steamid(steamid=steamid)
          if isresponse(steam_inventory):
               return steam_inventory
          
          new_skins = []
          skins = []
          for skin in steam_inventory[:30 - len(user.skins)]:
               if skin not in user.skins_names:
                    price = await self.http_client.item_price(item=skin)
                    if price is None:
                         continue
                    
                    new_skins.append(
                         {
                              "skin_id": await generate_skin_id(),
                              "name": skin,
                              "current_price": price,
                              "percent": 25,
                              "price_chart": f"{price},",
                              "owner": user.telegram_id
                         }
                    )
                    skins.append(skin)
                    await asyncio.sleep(3)
          
          if new_skins:
               await self.skin_repository.create(values=new_skins)
          return skins
          
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=SteamHttpClient(),
          json_storage=JsonStorage(),
          chart=Chart()
     )