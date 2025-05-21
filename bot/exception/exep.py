from .abstract_eception import AbstractBotExeption
from bot.core.bot import bot
from bot.core.config import base_config



class BotException(AbstractBotExeption):
     
     @classmethod
     async def send_notify(cls, msg: str) -> None:
          for admin_id in base_config.admins:
               await bot.send_message(
                    chat_id=admin_id,
                    text=msg
               )