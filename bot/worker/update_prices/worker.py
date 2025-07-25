import asyncio

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
          logging_.worker_update_prices.info("high update price start")
          
          await asyncio.sleep(20)
          await self._process(mode=SkinUpdateMode.HIGH)
          await self.__high_price_update()
          
          
     async def __medium_well_update(self) -> None:
          logging_.worker_update_prices.info("medium well update price start")
          
          await asyncio.sleep(3600 * 2)
          await self._process(mode=SkinUpdateMode.MEDIUM_WELL)
          await self.__medium_well_update()
          
          
     async def __medium_update(self) -> None:
          logging_.worker_update_prices.info("medium update price start")
          
          await asyncio.sleep(3600 * 3)
          await self._process(mode=SkinUpdateMode.MEDIUM)
          await self.__medium_update()
          
          
     async def __low_update(self) -> None:
          logging_.worker_update_prices.info("low update price start")
          
          await asyncio.sleep(3600 * 4)
          await self._process(mode=SkinUpdateMode.LOW)
          await self.__low_update()
          