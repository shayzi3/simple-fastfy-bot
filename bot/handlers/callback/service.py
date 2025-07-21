import asyncio
import os
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.gen import generate_skin_id
from bot.db.models import User
from bot.db.repository import SkinRepository, UserRepository, UserSkinRepository
from bot.infrastracture.http.steam import SteamHttpClient
from bot.responses import AnyResponse, DataUpdate, SkinCreate, TryLater, isresponse
from bot.schemas import SteamSkins
from bot.utils.filter.callback import Paginate


class CallbackService:
     def __init__(self) -> None:
          self.user_repository = UserRepository
          self.skin_repository = SkinRepository
          self.user_skin_repository = UserSkinRepository
          self.http_client = SteamHttpClient()
          
          
     
     async def register_new_steam_account(
          self,
          session: AsyncSession,
          user: User,
          steam_id: int
     ) -> AnyResponse:
          steam_data = await self.http_client.steam_user(steam_id=steam_id)
          if isresponse(steam_data):
               return steam_data
          
          await self.user_repository.update(
               session=session,
               values={
                    "steam_id": steam_data.steam_id,
                    "steam_name": steam_data.steam_name,
                    "steam_avatar": steam_data.steam_avatar,
                    "steam_profile_link": steam_data.steam_profile_link
               },
               id=user.id
          )
          return DataUpdate
     
     
     async def steam_skin(
          self,
          session: AsyncSession,
          user: User,
          skin_hash_name: str
     ) -> AnyResponse:
          skin_exists = await self.skin_repository.read(
               session=session,
               name=skin_hash_name
          )
          if skin_exists is None:
               await self.skin_repository.create(
                    session=session,
                    values={"name": skin_hash_name}
               )
          await self.user_skin_repository.create(
               session=session,
               values={
                    "uuid": uuid.uuid4(),
                    "skin_name": skin_hash_name,
                    "user_id": user.id
               }
          )
          return SkinCreate
     
     
     async def steam_skin_paginate(
          self,
          callback_data: Paginate
     ) -> tuple[SteamSkins, Paginate] | AnyResponse:
          if "left" in callback_data.mode:
               callback_data.offset = callback_data.offset - 5
               callback_data.current_page = callback_data.current_page - 1
               
          elif "right" in callback_data.mode:
               callback_data.offset = callback_data.offset + 5
               callback_data.current_page = callback_data.current_page + 1
          
          skins = await self.http_client.skin_search(query=callback_data.query)
          if isresponse(skins):
               return skins
          return (skins, callback_data)
     
     
     async def delete_item(
          self,
          user: User,
          item: str
     ) -> None:
          await self.skin_repository.delete(
               where={"owner": user.telegram_id, "name": item}
          )          
          
          
     async def chart_item(
          self,
          name: str,
          prices: list[int],
          telegram_id: int
     ) -> str:
          return await self.chart.chart_generate(
               prices=prices,
               filename=f"{telegram_id}.png",
               name=name
          )
          
          
     async def delete_chart_file(
          self,
          path: str
     ) -> None:
          if os.path.exists(path) is True:
               os.remove(path)   
               
           
     async def reset_chart(
          self,
          user: UserModel,
          skin_name: str
     ) -> AnyResponse | None:
          item_price = await self.http_client.item_price(item=skin_name)
          if isinstance(item_price, float) is False:
               return TryLater
          
          await self.skin_repository.update(
               where={"owner": user.telegram_id, "name": skin_name},
               values={"price_chart": f"{item_price},"}
          )
          
     async def steam_inventory(
          self,
          user: UserModel,
          steamid: int
     ) -> AnyResponse | list[str]:
          if len(user.skins) >= 30:
               return InventoryLimit
          
          steam_inventory = await self.http_client.inventory_by_steamid(steamid=steamid)
          if isresponse(steam_inventory):
               return steam_inventory
          
          new_skins = []
          skins = []
          for skin in steam_inventory[:30 - len(user.skins)]:
               if skin not in user.skins_names:
                    price = await self.http_client.item_price(item=skin)
                    if price is None:
                         continue
                    
                    new_skins.append(
                         {
                              "skin_id": await generate_skin_id(),
                              "name": skin,
                              "current_price": price,
                              "percent": 25,
                              "price_chart": f"{price},",
                              "owner": user.telegram_id
                         }
                    )
                    skins.append(skin)
                    await asyncio.sleep(3)
          
          if new_skins:
               await self.skin_repository.create(values=new_skins)
          return skins
          
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService()