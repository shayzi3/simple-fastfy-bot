from typing import Awaitable, Callable, Any
from datetime import timedelta, datetime
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware



class TimeoutMiddleware(BaseMiddleware):
     timeoutes = {
          "start": timedelta(seconds=1),
          "search": timedelta(seconds=1),
          "settings": timedelta(seconds=2),
          "inventory": timedelta(seconds=2),
          "settings_notify": timedelta(seconds=2),
          "settings_update_time": timedelta(seconds=4),
          "steam_item": timedelta(seconds=3),
          "inventory_item": timedelta(seconds=2),
          "inventory_left": timedelta(seconds=1),
          "inventory_right": timedelta(seconds=1),
          "delete_item": timedelta(seconds=1),
          "update_percent": timedelta(seconds=4)
     }
     command_users = {}
     
     
     async def __call__(
          self,
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ):
          command = data.get("handler").callback.__name__
          
          if self.timeoutes.get(command) is None:
               return await handler(event, data)
          
          if command not in self.command_users.keys():
               self.command_users.update({command: {}})
               
          if str(event.from_user.id) not in self.command_users[command]:
               self.command_users[command].update(
                    {str(event.from_user.id): datetime.utcnow() + self.timeoutes[command]}
               )
               return await handler(event, data)
          
          if self.command_users[command][str(event.from_user.id)] <= datetime.utcnow():
               self.command_users[command].update(
                    {str(event.from_user.id): datetime.utcnow() + self.timeoutes[command]}
               )
               return await handler(event, data)
          return await event.answer("Превышен лимит запросов!")