from bot.core.bot import bot
from bot.core.config import base_config


class BotException:
     
     @classmethod
     async def send_notify(cls, msg: str) -> None:
          pass