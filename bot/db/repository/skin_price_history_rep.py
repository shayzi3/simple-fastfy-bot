from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import SkinPriceHistory

from .repository import Repository


class SkinPriceHistoryRepository(Repository[SkinPriceHistory]):
     model = SkinPriceHistory
     
     
     @classmethod
     async def timestamp_filter(
          cls,
          session: AsyncSession,
          skin_name: str,
          timestamps: list[tuple[datetime, str]]
     ) -> list[SkinPriceHistory]:
          sttm = (
               select(SkinPriceHistory).
               where(
                    SkinPriceHistory.skin_name == skin_name,
                    *[(SkinPriceHistory.timestamp >= time).label(label) for time, label in timestamps]
               ).
               order_by(SkinPriceHistory.timestamp)
          )
          result = await session.execute(sttm)
          return result.scalars().all()
          
          
          
          
          