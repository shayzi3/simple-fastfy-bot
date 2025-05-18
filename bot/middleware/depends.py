import inspect

from typing import Any, Awaitable, Callable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from bot.handlers import __depends__


class DependMiddleware(BaseMiddleware):
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ) -> None:
          callback_object = data.get("handler").callback
          arguments = inspect.signature(callback_object).parameters
          
          for key, value in arguments.items():
               if str(value.annotation) in __depends__.keys():
                    data[key] = await __depends__[str(value.annotation)]()
          return await handler(event, data)