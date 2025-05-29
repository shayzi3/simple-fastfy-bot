
from bot.core.gen import generate_skin_id
from bot.core.timezone import time_now
from bot.db.json_storage import JsonStorage
from bot.db.repository import SkinRepository, UserRepository
from bot.http.steam import SteamHttpClient, SteamParseClient
from bot.schemas import SteamUser, Time, UserDataclass


class StateService:
     def __init__(
          self, 
          user_repository: UserRepository,
          parse_client: SteamParseClient,
          http_client: SteamHttpClient,
          skin_repository: SkinRepository,
          json_storage: JsonStorage
     ):
          self.user_repository = user_repository
          self.parse_client = parse_client
          self.http_client = http_client
          self.skin_repository = skin_repository
          self.json_storage = json_storage
          
     
     async def update_time(
          self,
          user: UserDataclass,
          new_time: str
     ) -> bool:
          await self.json_storage.update(
               search_string=f"{user.telegram_id}",
               new_value=(
                    f"{new_time};"
                    f"{(time_now() + Time.from_str(new_time).to_timedelta()).isoformat()};"
                    f"{user.telegram_id}"
               )
          )
          return await self.user_repository.update(
               where=user.where,
               values={"update_time": new_time}
          )
          
          
     async def search_item(self, item: str) -> str | list[str]:
          return await self.parse_client.search_item(item=item)   
     
     
     async def create_item_with_percent(
          self,
          item: str,
          user: UserDataclass,
          percent: int
     ):
          item_price = await self.http_client.item_price(item=item)
          if item_price is None:
               return "Повторите попытку позже."
          
          await self.skin_repository.create(
               values={
                    "skin_id": await generate_skin_id(),
                    "name": item,
                    "current_price": item_price,
                    "percent": percent,
                    "price_chart": f"{item_price},",
                    "owner": user.telegram_id
               }
          )
          return f"Предмет {item} успешно добавлен в инвентарь."
          
          
     async def update_item_percent(
          self,
          user: UserDataclass,
          item: str,
          percent: int
     ):
          await self.skin_repository.update(
               where={"owner": user.telegram_id, "name": item},
               values={"percent": percent}
          )
          
          
     async def steam_user(self, steamid: int) -> str | SteamUser:
          steam_user = await self.http_client.steam_user(steamid=steamid)
          if steam_user is None:
               return "Такого ID не существует"
          return steam_user
          
          
          
          
async def get_state_service() -> StateService:
     return StateService(
          user_repository=UserRepository,
          parse_client=SteamParseClient(),
          http_client=SteamHttpClient(),
          skin_repository=SkinRepository,
          json_storage=JsonStorage()
     )
               