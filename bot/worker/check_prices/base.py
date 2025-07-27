

from bot.db.repository import SkinRepository
from bot.logging_ import logging_
from bot.schemas.enums import SkinUpdateMode


class CheckPricesBaseWorker:
     def __init__(self):
          self.skin_repository = SkinRepository
          
          
     async def _process(self, mode: SkinUpdateMode) -> None:
          ...
          
          
     async def __check_prices(self, skin_name: str) -> None:
          ...