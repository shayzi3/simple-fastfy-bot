from bot.db.repository import UserRepository


class CommandService:
     def __init__(
          self,
          user_repository: UserRepository
     ):
          self.user_repository = user_repository
     
     
     
     
     
async def get_command_service() -> CommandService:
     return CommandService(
          user_repository=UserRepository
     )