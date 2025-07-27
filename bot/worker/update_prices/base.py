import asyncio
import uuid
from datetime import datetime

from bot.db.repository import SkinPriceHistoryRepository, SkinRepository
from bot.db.session import async_db_session
from bot.infrastracture.http.steam import SteamHttpClient
from bot.logging_ import logging_
from bot.schemas.enums import SkinUpdateMode


class PriceUpdateBaseWorker:
     def __init__(self):
          self.skin_repository = SkinRepository
          self.skin_price_repository = SkinPriceHistoryRepository
          self.http_client = SteamHttpClient()
     
     
     async def _process(self, mode: SkinUpdateMode) -> None:
          logging_.worker_update_prices.info(f"UPDATE PRICE START MODE {mode}")
          
          async with async_db_session() as session:
               skins = await self.skin_repository.read(
                    session=session,
                    all=True,
                    update_mode=mode
               )
          gather_funcs = []
          for skin in skins:
               gather_funcs.append(self.__process_update_skin_price(skin.price, skin.name))
          await asyncio.gather(*gather_funcs)
               
               
     async def __process_update_skin_price(
          self,
          last_price: float,
          skin_name: str
     ) -> None:
          skin_price = await self.http_client.skin_price_and_volume(skin_name=skin_name)
          new_update_mode = SkinUpdateMode.new_update_mode(
               last_price=last_price,
               new_price=skin_price[0],
               volume=skin_price[1]
          )
          
          async with async_db_session() as session:
               await self.skin_repository.update(
                    session=session,
                    values={
                         "price": skin_price[0],
                         "update_mode": new_update_mode
                    },
                    returning=False,
                    name=skin_name
               )
               await self.skin_price_repository.create(
                    session=session,
                    values={
                         "uuid": uuid.uuid4(),
                         "skin_name": skin_name,
                         "price": skin_price[0],
                         "volume": skin_price[1],
                         "timestamp": datetime.now()
                    },
                    returning=False
               )
          logging_.worker_update_prices.info(f"UPDATE SKIN PRICE {skin_name}")
               