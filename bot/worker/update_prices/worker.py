import asyncio
from datetime import timedelta

from bot.logging_ import logging_
from bot.schemas.enums import SkinUpdateMode

from .base import PriceUpdateBaseWorker


class PriceUpdateWorker(PriceUpdateBaseWorker):
     def __init__(self):
          super().__init__()
     
     
     async def run(self) -> None:
          logging_.worker_update_prices.info("UPDATE PRICE START")
          
          asyncio.create_task(self.__high_price_update())
          asyncio.create_task(self.__medium_well_update())
          asyncio.create_task(self.__medium_update())
          asyncio.create_task(self.__low_update())
     
     
     async def __high_price_update(self) -> None:
          logging_.worker_update_prices.info("HIGH START")
          
          await asyncio.sleep(timedelta(hours=1).total_seconds())
          await self._process(mode=SkinUpdateMode.HIGH)
          await self.__high_price_update()
          
          
     async def __medium_well_update(self) -> None:
          logging_.worker_update_prices.info("MEDIUM WELL START")
          
          await asyncio.sleep(timedelta(hours=2).total_seconds())
          await self._process(mode=SkinUpdateMode.MEDIUM_WELL)
          await self.__medium_well_update()
          
          
     async def __medium_update(self) -> None:
          logging_.worker_update_prices.info("MEDIUM START")
          
          await asyncio.sleep(timedelta(hours=3).total_seconds())
          await self._process(mode=SkinUpdateMode.MEDIUM)
          await self.__medium_update()
          
          
     async def __low_update(self) -> None:
          logging_.worker_update_prices.info("LOW START")
          
          await asyncio.sleep(timedelta(hours=4).total_seconds())
          await self._process(mode=SkinUpdateMode.LOW)
          await self.__low_update()
          