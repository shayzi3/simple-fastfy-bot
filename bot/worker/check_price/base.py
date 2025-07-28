import asyncio

from bot.core.bot import bot
from bot.db.models import UserSkin
from bot.db.repository import SkinPriceHistoryRepository, UserSkinRepository
from bot.db.session import async_db_session
from bot.logging_ import logging_
from bot.schemas import NotifyData, NotifySkin


class CheckPriceBaseWorker:
     def __init__(self):
          self.user_skin_repository = UserSkinRepository
          self.skin_history_repository = SkinPriceHistoryRepository
          
          
     async def _process(self) -> None:
          logging_.worker_check_prices.info("START PROCESS")
          
          async with async_db_session() as session:
               users_skins = await self.user_skin_repository.read(
                    session=session,
                    with_relation=True,
                    all=True
               )
          
          gather_funcs = []
          if users_skins:
               for skin in users_skins:
                    gather_funcs.append(self.__check_prices_process(user_skin=skin))
               await asyncio.gather(*gather_funcs)
     
     
     async def __check_prices_process(
          self, 
          user_skin: UserSkin
     ) -> None:
          data = NotifyData(skins=[])
          if user_skin.skin.price_at_1_day >= user_skin.user.skin_percent:
               data.skins.add(
                    NotifySkin(
                         skin_name=user_skin.skin_name,
                         price_percent=user_skin.skin.price_at_1_day,
                         change_price_at_day=1
                    )
               )
                    
          if user_skin.skin.price_at_7_day >= user_skin.user.skin_percent:
               data.skins.add(
                    NotifySkin(
                         skin_name=user_skin.skin_name,
                         price_percent=user_skin.skin.price_at_7_day,
                         change_price_at_day=7
                    )
               )
                    
          if user_skin.skin.price_at_30_day >= user_skin.user.skin_percent:
               data.skins.add(
                    NotifySkin(
                         skin_name=user_skin.skin_name,
                         price_percent=user_skin.skin.price_at_30_day,
                         change_price_at_day=30
                    )
               )
          if data.skins:
               await bot.send_message(
                    chat_id=user_skin.user.id,
                    text=data.pretty_skins()
               )
                    
          