import asyncio
from datetime import datetime, timedelta

from bot.db.repository import SkinPriceHistoryRepository, SkinRepository
from bot.db.session import async_db_session
from bot.logging_ import logging_


class UpdatePriceAtDaysBaseWorker:
     def __init__(self):
          self.skin_repository = SkinRepository
          self.skin_price_history = SkinPriceHistoryRepository
          
          
     async def _process(self) -> None:
          logging_.worker_update_price_at_day.info("START PROCESS")
          
          gather_funcs = []
          async with async_db_session() as session:
               skins = await self.skin_repository.read(
                    session=session,
                    all=True
               )
               time = 0.5
               for skin in skins:
                    gather_funcs.append(
                         self.__update_price_at_days_process(
                              skin_name=skin.name,
                              sleep=time
                         )
                    )
                    time += 0.5
          await asyncio.gather(*gather_funcs)
               
         
         
     async def __update_price_at_days_process(
          self, 
          skin_name: str,
          sleep: int
     ) -> None:
          await asyncio.sleep(sleep)
          
          async with async_db_session() as session:
               skins_price = await self.skin_price_history.timestamp_filter(
                    session=session,
                    skin_name=skin_name,
                    timestamps=[
                         (datetime.now() - timedelta(days=1), "day"),
                         (datetime.now() - timedelta(days=7), "week"),
                         (datetime.now() - timedelta(days=30), "month")
                    ]
               )
               day, week, month = [], [], []
               for skin in skins_price:
                    if skin.day:
                         day.append(skin.price)
                    if skin.week:
                         week.append(skin.price)
                    if skin.month:
                         month.append(skin.price)
               
               price_day, price_week, price_month = None, None, None
               if len(day) >= 2:
                    price_day = ((day[0] - day[-1])/day[0])*100
               if len(week) >= 2:
                    price_week = ((week[0] - week[-1])/week[0])*100
               if len(month) >= 2:
                    price_month = ((month[0] - month[-1])/month[0])*100
               
               await self.skin_repository.update(
                    session=session,
                    values={
                         "price_at_1_day": price_day,
                         "price_at_7_day": price_week,
                         "price_at_30_day": price_month
                    },
                    returning=False,
                    name=skin_name
               )
          logging_.worker_update_price_at_day.info(f"SKIN PRICE AT DAYS UPDATED {skin_name}")