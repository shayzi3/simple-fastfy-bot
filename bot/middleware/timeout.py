from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from bot.schemas.base import TimeOut


class TimeoutMiddleware(BaseMiddleware):
     timeoutes = {
          "start": TimeOut(
               time=timedelta(seconds=1),
               msg="1с"
          ),
          "search": TimeOut(
               time=timedelta(seconds=1),
               msg="1с"
          ),
          "settings": TimeOut(
               time=timedelta(seconds=2),
               msg="2с"
          ),
          "inventory": TimeOut(
               time=timedelta(seconds=2),
               msg="2с"
          ),
          "settings_notify": TimeOut(
               time=timedelta(seconds=2),
               msg="2с"
          ),
          "settings_update_time": TimeOut(
               time=timedelta(seconds=4),
               msg="4с"
          ),
          "steam_item": TimeOut(
               time=timedelta(seconds=3),
               msg="3с"
          ),
          "inventory_item": TimeOut(
               time=timedelta(seconds=2),
               msg="2с"
          ),
          "inventory_left": TimeOut(
               time=timedelta(seconds=1),
               msg="1с"
          ),
          "inventory_right": TimeOut(
               time=timedelta(seconds=1),
               msg="1с"
          ),
          "delete_item": TimeOut(
               time=timedelta(seconds=1),
               msg="1с"
          ),
          "create_skin_or_update_percent": TimeOut(
               time=timedelta(seconds=4),
               msg="4с"
          ),
          "chart_item": TimeOut(
               time=timedelta(seconds=15),
               msg="15с"
          ),
          "steam_profile": TimeOut(
               time=timedelta(minutes=2),
               msg="2m"
          )
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
               
          command_timeout = self.timeoutes[command]
          if str(event.from_user.id) not in self.command_users[command]:
               self.command_users[command].update(
                    {str(event.from_user.id): datetime.utcnow() + command_timeout.time}
               )
               return await handler(event, data)
          
          if self.command_users[command][str(event.from_user.id)] <= datetime.utcnow():
               self.command_users[command].update(
                    {str(event.from_user.id): datetime.utcnow() + command_timeout.time}
               )
               return await handler(event, data)
          return await event.answer(f"Лимит использования команды {command_timeout.msg}")