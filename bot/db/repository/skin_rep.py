from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Skin

from .repository import Repository


class SkinRepository(Repository[Skin]):
     model = Skin
     
     
     @classmethod
     async def read_all_with_or(
          cls,
          session: AsyncSession,
          read_data: list[Any],
          values: list[Any] = []
     ) -> list[Skin] | list[Any]:
          sttm = select(Skin).where(or_(*read_data))
          if values:
               sttm = select(*values).where(or_(*read_data))
               
          result = await session.execute(sttm)
          return result.scalars().all()
          