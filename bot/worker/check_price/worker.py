import asyncio
from datetime import timedelta

from bot.logging_ import logging_

from .base import CheckPriceBaseWorker


class CheckPriceWorker(CheckPriceBaseWorker):
     def __init__(self):
          super().__init__()
          
          
     async def run(self) -> None:
          logging_.worker_check_prices.info("CHECK PRICES START")
          
          asyncio.create_task(self.__check_price())
          
          
     async def __check_price(self) -> None:
          await asyncio.sleep(timedelta(hours=2).total_seconds())
          await self._process()
          await self.__check_price()
          
          