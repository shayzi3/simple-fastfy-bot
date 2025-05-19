from bot.schemas import UserDataclass
from bot.db.repository import UserRepository
from bot.http.steam import SteamParseClient



class StateService:
     def __init__(
          self, 
          user_repository: UserRepository,
          parse_client: SteamParseClient
     ):
          self.user_repository = user_repository
          self.parse_client = parse_client
          
     
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
          
          
async def get_state_service() -> StateService:
     return StateService(
          user_repository=UserRepository,
          parse_client=SteamParseClient()
     )
               