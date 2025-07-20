import inspect
from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.utils.depend import Depend


class DependMiddleware(BaseMiddleware):
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message | CallbackQuery, 
          data: dict[str, Any]
     ) -> None:
          callback_object = data.get("handler").callback
          signature = inspect.signature(callback_object)
          
          for arg, value in signature.parameters.items():
               meta = getattr(value.annotation, "__metadata__", None) # Annotated
               if meta is not None:
                    for depend in meta:
                         if isinstance(depend, Depend):
                              data[arg] = await depend.call(data)
               else: # dafault value
                    if isinstance(value.default, Depend):
                         data[arg] = await value.default.call(data)
          return await handler(event, data)