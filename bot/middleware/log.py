from typing import Any, Callable, Awaitable
from aiogram.types import Message
from aiogram.dispatcher.middlewares.base import BaseMiddleware

from bot.exception import BotException
from bot.log.logging_ import logging_




class LogMiddleware(BaseMiddleware):
     
     
     async def __call__(
          self, 
          handler: Callable[[Message, dict[str, Any]], Awaitable[Any]], 
          event: Message, 
          data: dict[str, Any]
     ):
          router = data.get("event_router").name
          command = data.get("command").command
          
          logging_.bot.info(f"ROUTER: {router}; COMMAND: {command}; USER: {event.from_user.id}")
          
          try:
               return await handler(event, data)
          except Exception as ex:
               logging_.bot.error(msg="error", exc_info=ex)
               await BotException.send_notify(msg=f"ERROR: {ex} COMMAND: {command}")
               return await event.answer("Произошла ошибка. Повторите запрос позднее")