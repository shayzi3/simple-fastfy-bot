from bot.core.bot import bot
from bot.core.config import base_config


class Alert:
     
     @classmethod
     async def notify(cls, msg: str) -> None:
          async with bot as session:
               await session.send_message(
                    chat_id=base_config.alert_chanel,
                    text=msg
               )