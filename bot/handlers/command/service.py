from bot.db.repository import UserRepository


class CommandService:
     def __init__(
          self,
          user_repository: UserRepository
     ):
          self.user_repository = user_repository
     
     
     async def start(
          self,
          telegram_id: int
     ) -> None:
          await self.user_repository.create(
               values={
                    "telegram_id": telegram_id,
                    "notify": False,
                    "update_time": "0-0-25"
               }
          )

     
     
     
async def get_command_service() -> CommandService:
     return CommandService(
          user_repository=UserRepository
     )