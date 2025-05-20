import asyncio

from datetime import datetime
from typing import Any

from bot.db.repository import UserRepository, SkinRepository
from bot.http.steam import SteamHttpClient
from bot.schemas import Time
from bot.log.logging_ import logging_
from bot.exception import BotException
from bot.db.json_storage import JsonStorage
from bot.core.bot import bot



class MonitoringWorker:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: SteamHttpClient,
          json_storage: JsonStorage
     ) -> None:
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          self.json_storage = json_storage
     
     
     async def run(self) -> None:
          while True:
               logging_.worker.info("Start worker")
               
               tasks = await self.json_storage.get_all()
               if tasks:
                    parallel = []
                    for index, time_user in enumerate(tasks):
                         try:
                              period = time_user.split(";")[0]
                              time = datetime.fromisoformat(time_user.split(";")[1])
                              user = int(time_user.split(";")[2])
                         except Exception as ex:
                              await BotException.send_notify(msg=str(ex))
                              
                         if time <= datetime.now():
                              new_time = (
                                   datetime.now() + Time.from_str(period).to_timedelta()
                              ).isoformat()
                              new_value = f"{period};{new_time};{user}"
                              
                              await self.json_storage.update(
                                   search_string=f"{user}", 
                                   new_value=new_value
                              )
                              logging_.worker.info(f"Find user {user} with time {time}")
                              parallel.append(self.__price_updater(user))
                              
                    if parallel:
                         logging_.worker.info("Start gather for users")
                         await asyncio.gather(*parallel)
               await asyncio.sleep(180)
          
          
     async def __price_updater(
          self,
          telegram_id: int
     ) -> None:
          logging_.worker.info(f"Start gather for user {telegram_id}")
          
          user = await self.user_repository.read(
               where={"telegram_id": telegram_id},
          )
          if (user is None) or (not user.skins):
               return
          
          notify = []
          update_skins = []
          for skin in user.skins:
               new_price = await self.http_client.item_price(item=skin.name)
               if isinstance(new_price, float) is False:
                    continue
               
               max_ = max([skin.current_price, new_price])
               min_ = min([skin.current_price, new_price])
               percent_difference = ((max_ - min_) * 100) // max_
               
               if percent_difference >= skin.percent:
                    logging_.worker.info(
                         f"Detect difference percent for {skin.name} at user {telegram_id}"
                    )
                    update_skins.append(
                         {
                              "_owner": telegram_id,
                              "_name": skin.name,
                              "_current_price": new_price
                         }
                    )
                    notify.append(
                         {
                              "name": skin.name,
                              "last_price": skin.current_price,
                              "update_price": new_price,
                              "difference": percent_difference
                         }
                    )
               await asyncio.sleep(1)
               
               
          if update_skins:
               logging_.worker.info(f"Update skins and send notify for user {telegram_id}")
               await self.skin_repository.update_many(data=update_skins)
               await self._send_notify(
                    notify_data=notify,
                    telegram_id=telegram_id
               )
               
               
     async def _send_notify(
          self, 
          notify_data: list[dict[str, Any]], 
          telegram_id: int
     ) -> None:
          for skin in notify_data:
               await bot.send_message(
                    chat_id=telegram_id,
                    text=f"{skin.get('name')} \n{skin.get('last_price')} -> {skin.get('update_price')} {skin.get('difference')}%"
               )