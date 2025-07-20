from datetime import datetime, timedelta

from aiogram.filters import Filter
from aiogram.types import Message


class Storage:
     rate_users: dict[str, datetime] = {}



class RateLimit(Filter):
     def __init__(self, seconds: float):
          self.rate = Storage
          self.rate_time = timedelta(seconds=seconds)
          
          
     async def __call__(self, message: Message) -> bool:
          user = str(message.from_user.id)
          if user not in self.rate.rate_users:
               self.rate.rate_users[user] = datetime.utcnow() + self.rate_time
               return True
          
          if self.rate.rate_users[user] >= datetime.utcnow():
               await message.answer(
                    ("До следующего использования команды:" + 
                     f"{(self.rate.rate_users[user] - datetime.utcnow()).seconds} секунд")
               )
               return False
          
          self.rate.rate_users[user] = datetime.utcnow() + self.rate_time
          return True
          