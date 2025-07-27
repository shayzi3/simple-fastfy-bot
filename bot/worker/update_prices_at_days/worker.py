import asyncio
from datetime import timedelta

from bot.logging_ import logging_

from .base import UpdatePricesAtDaysBaseWorker


class UpdatePricesAtDaysWorker(UpdatePricesAtDaysBaseWorker):
     def __init__(self):
          super().__init__()
          
          
     async def run(self) -> None:
          logging_.worker_update_prices_at_days.info("UPDATE PRICES AT DAYS START")
          
          asyncio.create_task(self.__update_price_at_days())
          
          
     async def __update_price_at_days(self) -> None:
          await asyncio.sleep(timedelta(hours=2, minutes=30).total_seconds())
          await self._process()
          await self.__update_price_at_days()