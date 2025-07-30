from typing import Any, Awaitable, Callable

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from bot.alert import Alert
from bot.logging_ import logging_


class LogMiddleware(BaseMiddleware):
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ):
          router = data.get("event_router").name
          command = data.get("handler").callback.__name__
          
          logging_.bot.info(f"ROUTER: {router}; COMMAND: {command}; USER: {event.from_user.id}-{event.from_user.username}")
          
          try:
               return await handler(event, data)
          except Exception as ex:
               logging_.bot.error(msg="error", exc_info=ex)
               await Alert.notify(msg=str(ex))
               return await event.answer("Произошла ошибка. Повторите запрос позднее")