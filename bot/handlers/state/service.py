from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.repository import SkinRepository, UserRepository
from bot.infrastracture.http.steam import SteamHttpClient
from bot.responses import AnyResponse, DataUpdate
from bot.schemas import SteamSkins, SteamUser


class StateService:
     def __init__(self) -> None:
          self.user_repository = UserRepository
          self.http_client = SteamHttpClient()
          self.skin_repository = SkinRepository
          
          
     async def skin_search(self, query: str) -> AnyResponse | SteamSkins:
          return await self.http_client.skin_search(query=query)
     
     
     async def steam_user(self, steam_id: int) -> AnyResponse | SteamUser:
          return await self.http_client.steam_user(steam_id=steam_id)
     
     
     async def update_skin_percent(
          self,
          session: AsyncSession,
          user: User,
          percent: int
     ) -> AnyResponse:
          await self.user_repository.update(
               session=session,
               values={"skin_percent": percent},
               id=user.id
          )
          return DataUpdate
          
          
               
          
          
          
async def get_state_service() -> StateService:
     return StateService()
               