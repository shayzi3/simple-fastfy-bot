import asyncio
from datetime import timedelta

from bot.logging_ import logging_
from bot.schemas.enums import SkinUpdateMode

from .base import UpdateCheckSkinPriceBaseWorker


class UpdateCheckSkinPriceWorker(UpdateCheckSkinPriceBaseWorker):
     def __init__(self):
          super().__init__()
     
     
     async def run(self) -> None:
          logging_.worker_update_check_prices.info("START WORKER")
          
          functions = [
               self.__update_check_skin_price(
                    mode=SkinUpdateMode.HIGH, 
                    sleep=timedelta(hours=1)
               ),
               self.__update_check_skin_price(
                    mode=SkinUpdateMode.MEDIUM_WELL, 
                    sleep=timedelta(hours=2)
               ),
               self.__update_check_skin_price(
                    mode=SkinUpdateMode.MEDIUM, 
                    sleep=timedelta(hours=3)
               ),
               self.__update_check_skin_price(
                    mode=SkinUpdateMode.LOW, 
                    sleep=timedelta(hours=4)
               )
          ]
          for func in functions:
               asyncio.create_task(func)
     
     
     async def __update_check_skin_price(
          self, 
          mode: SkinUpdateMode, 
          sleep: timedelta
     ) -> None:
          logging_.worker_update_check_prices_at_days.info(f"MODE {mode} START")
          
          await asyncio.sleep(sleep.total_seconds())
          await self._process(mode=mode)
          await self.__update_check_skin_price(mode=mode, sleep=sleep)
          