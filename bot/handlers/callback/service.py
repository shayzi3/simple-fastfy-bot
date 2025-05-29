import asyncio
import os

from bot.core.gen import generate_skin_id
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
          
     async def steam_inventory(
          self,
          user: UserDataclass,
          steamid: int
     ) -> str | list[str]:
          if len(user.skins) >= 30:
               return "Скинов не может быть больше 30!"
          
          steam_inventory = await self.http_client.inventory_by_steamid(steamid=steamid)
          if isinstance(steam_inventory, str):
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