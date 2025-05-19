from bot.schemas import UserDataclass
from bot.db.repository import UserRepository



class StateService:
     def __init__(self, user_repository: UserRepository):
          self.user_repository = user_repository
          
     
     async def update_time(
          self,
          user: UserDataclass,
          new_time: str
     ) -> bool:
          return await self.user_repository.update(
               where=user.where,
               values={"update_time": new_time}
          )
          
          
async def get_state_service() -> StateService:
     return StateService(
          user_repository=UserRepository
     )
               