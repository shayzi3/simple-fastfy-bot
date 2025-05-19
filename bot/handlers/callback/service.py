from bot.db.repository import UserRepository
from bot.schemas import UserDataclass



class CallbackService:
     def __init__(self, user_repository: UserRepository):
          self.user_repository = user_repository
          
          
     async def settings_notify(
          self,
          user: UserDataclass
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          await self.user_repository.update(
               where=user.where,
               values=update_data
          )
          return update_data.get("notify")
     
     
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService(
          user_repository=UserRepository
     )