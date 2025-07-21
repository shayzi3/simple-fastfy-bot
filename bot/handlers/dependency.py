from typing import Annotated

from aiogram.types.base import TelegramObject
from aiogram_tool.depend import Depend
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User
from bot.db.repository import UserRepository
from bot.db.session import async_db_session


async def get_user(
     event: TelegramObject, 
     session: Annotated[AsyncSession, Depend(async_db_session)]
) -> User:
     user = await UserRepository.read(
          session=session,
          id=event.from_user.id
     )
     if user is None:
          await UserRepository.create(
               session=session,
               values={
                    "id": event.from_user.id,
                    "name": event.from_user.username
               }
          )
          return await get_user(event=event, session=session)
     return user
     
     
     
async def get_user_rel(
     event: TelegramObject, 
     session: Annotated[AsyncSession, Depend(async_db_session)]
) -> User:
     user = await UserRepository.read(
          session=session,
          with_relation=True,
          id=event.from_user.id
     )
     if user is None:
          await UserRepository.create(
               session=session,
               values={
                    "id": event.from_user.id,
                    "name": event.from_user.username
               }
          )
          return await get_user_rel(event=event, session=session)
     return user