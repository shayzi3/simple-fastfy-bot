
from bot.db.json_storage import JsonStorage
from bot.db.repository import SkinRepository, UserRepository
from bot.infrastracture.http.steam import SteamHttpClient, SteamParseClient
from bot.schemas import UserModel
from bot.utils.responses import AnyResponse, InvalidSteamID


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
          
          
          
     async def search_item(self, item: str) -> AnyResponse | list[str]:
          return await self.parse_client.search_item(item=item)
     
     
     
     async def create_item_with_percent(
          self,
          item: str,
          user: UserModel,
          percent: int
     ):
          ...
          
          
     async def update_item_percent(
          self,
          user: UserModel,
          item: str,
          percent: int
     ):
          await self.skin_repository.update(
               where={"owner": user.telegram_id, "name": item},
               values={"percent": percent}
          )
          
          
     async def steam_user(self, steamid: int) -> AnyResponse:
          steam_user = await self.http_client.steam_user(steamid=steamid)
          if steam_user is None:
               return InvalidSteamID
          return steam_user
          
          
          
          
async def get_state_service() -> StateService:
     return StateService(
          user_repository=UserRepository,
          parse_client=SteamParseClient(),
          http_client=SteamHttpClient(),
          skin_repository=SkinRepository,
          json_storage=JsonStorage()
     )
               