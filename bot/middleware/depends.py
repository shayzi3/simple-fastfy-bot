import inspect

from typing import Any, Awaitable, Callable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.handlers import __depends__
from bot.db.repository import UserRepository
from bot.schemas import UserDataclass



class DependMiddleware(BaseMiddleware):
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message | CallbackQuery, 
          data: dict[str, Any]
     ) -> None:
          callback_object = data.get("handler").callback
          arguments = inspect.signature(callback_object).parameters
          
          for key, value in arguments.items():
               if value.annotation is UserDataclass:
                    user = await UserRepository.read(where={"telegram_id": event.from_user.id})
                    if user is None:
                         await UserRepository.create(
                              values={
                                   "telegram_id": event.from_user.id,
                                   "notify": False,
                                   "update_time": "0-0-25"
                              }
                         )
                    data[key] = await UserRepository.read(where={"telegram_id": event.from_user.id})
                    continue
                    
               if value.annotation in __depends__.keys():
                    data[key] = await __depends__[value.annotation]()
          return await handler(event, data)