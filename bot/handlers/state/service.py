from bot.core.gen import generate_skin_id
from bot.schemas import UserDataclass
from bot.db.repository import UserRepository, SkinRepository
from bot.http.steam import SteamParseClient, SteamHttpClient



class StateService:
     def __init__(
          self, 
          user_repository: UserRepository,
          parse_client: SteamParseClient,
          http_client: SteamHttpClient,
          skin_repository: SkinRepository
     ):
          self.user_repository = user_repository
          self.parse_client = parse_client
          self.http_client = http_client
          self.skin_repository = skin_repository
          
     
     async def update_time(
          self,
          user: UserDataclass,
          new_time: str
     ) -> bool:
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
                    "owner": user.telegram_id
               }
          )
          return "Предмет успешно добавлен в инвентарь."
          
          
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
          
          
          
async def get_state_service() -> StateService:
     return StateService(
          user_repository=UserRepository,
          parse_client=SteamParseClient(),
          http_client=SteamHttpClient(),
          skin_repository=SkinRepository
     )
               