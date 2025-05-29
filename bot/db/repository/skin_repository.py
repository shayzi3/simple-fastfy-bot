from typing import Any

from sqlalchemy import and_, bindparam, insert, update

from bot.db.models import Skin
from bot.db.session import Session
from bot.log.logging_ import logging_
from bot.schemas import SkinDataclass

from .repository import Repository


class SkinRepository(Repository[SkinDataclass]):
     model = Skin
     
     
     @classmethod
     async def update_many(
          cls,
          data: list[dict[str, Any]],
     ) -> None:
          async with Session.engine.begin() as connection:
               sttm = (
                    update(Skin).
                    where(
                         and_(
                              Skin.owner == bindparam("_owner"),
                              Skin.name == bindparam("_name")
                         )
                    ).
                    values(
                         current_price=bindparam("_current_price"),
                         price_chart=bindparam("_price_chart")
                    )
               )
               await connection.execute(sttm, data)
               logging_.db.info(f"UPDATE PRICE AT SKINS: TELEGRAM_ID: {data[0].get('_owner')}")