import asyncio
import uuid
from datetime import datetime

from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.bot import bot
from bot.db.models import Skin
from bot.db.repository import (
    SkinPriceHistoryRepository,
    SkinRepository,
    UserSkinRepository,
)
from bot.db.session import async_db_session
from bot.infrastracture.http.steam import SteamHttpClient
from bot.logging_ import logging_
from bot.schemas.enums import SkinUpdateMode


class UpdateCheckSkinPriceBaseWorker:
     def __init__(self):
          self.skin_repository = SkinRepository
          self.skin_price_repository = SkinPriceHistoryRepository
          self.user_skin_repository = UserSkinRepository
          self.http_client = SteamHttpClient()
     
     
     async def _process(self, mode: SkinUpdateMode) -> None:
          async with async_db_session() as session:
               skins = await self.skin_repository.read(
                    session=session,
                    all=True,
                    update_mode=mode
               )
          gather_funcs = []
          if skins:
               for skin in skins:
                    gather_funcs.append(self.__update_skin_price_process(skin))
               await asyncio.gather(*gather_funcs)
               
               
     async def __update_skin_price_process(
          self,
          skin: Skin
     ) -> None:
          skin_price = await self.http_client.skin_price_and_volume(skin_name=skin.name)
          new_update_mode = SkinUpdateMode.new_update_mode(
               last_price=skin.price,
               new_price=skin_price[0],
               volume=skin_price[1]
          )
          
          update_time = datetime.now()
          async with async_db_session() as session:
               await self.skin_repository.update(
                    session=session,
                    values={
                         "price": skin_price[0],
                         "update_mode": new_update_mode,
                         "last_update": update_time
                    },
                    returning=False,
                    name=skin.name
               )
               await self.skin_price_repository.create(
                    session=session,
                    values={
                         "uuid": uuid.uuid4(),
                         "skin_name": skin.name,
                         "price": skin_price[0],
                         "volume": skin_price[1],
                         "timestamp": update_time
                    },
                    returning=False
               )
               if skin.price is not None:
                    percent = ((skin_price[0] - skin.price)/skin.price)*100
                    await self.__check_skin_price(
                         session=session,
                         skin=skin,
                         percent=percent,
                         new_skin_price=skin_price[0],
                         update_time=update_time
                    )
          logging_.worker_update_check_skin_price.info(f"UPDATE SKIN PRICE {skin.name}")
          
          
     async def __check_skin_price(
          self,
          session: AsyncSession,
          skin: Skin,
          percent: float,
          new_skin_price: float,
          update_time: datetime
     ) -> None:
          gather_funcs = []
          skins_at_users = await self.user_skin_repository.read(
               session=session,
               with_relation=True,
               all=True,
               skin_name=skin.name
          )
          if skins_at_users:
               for skin_at_user in skins_at_users:
                    if skin_at_user.user.check_percent(percent):
                         gather_funcs.append(
                              self.__send_notify(
                                   last_price=skin.price,
                                   new_price=new_skin_price,
                                   percent=percent,
                                   last_update=skin.last_update.strftime("%d-%m-%Y %H:%M:%S"),
                                   update=update_time.strftime("%d-%m-%Y %H:%M:%S"),
                                   skin_name=skin.name,
                                   telegram_id=skin_at_user.user.id
                              )
                         )
               if gather_funcs:
                    await asyncio.gather(*gather_funcs)
          
     async def __send_notify(
          self,
          telegram_id: int,
          skin_name: str,
          last_price: float,
          new_price: float,
          percent: float,
          last_update: datetime,
          update: datetime
     ) -> None:
          text = (
               f"{skin_name}\n"
               f"Цена <b>{last_update}</b> {last_price}р\n"
               f"Цена <b>{update}</b> {new_price}р\n"
               f"Изменение цены составило <b>{percent}</b>%"
          )
          async with bot as session:
               await session.send_message(
                    chat_id=telegram_id, 
                    text=text,
                    parse_mode=ParseMode.HTML
               )
          logging_.worker_update_check_skin_price.info(f"SEND NOTIFY {telegram_id}. Skin: {skin_name}")
               