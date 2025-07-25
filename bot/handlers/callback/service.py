import uuid
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Skin, User
from bot.db.repository import SkinRepository, UserRepository, UserSkinRepository
from bot.infrastracture.http.steam import SteamHttpClient
from bot.responses import (
    AnyResponse,
    DataUpdate,
    SkinCreate,
    SkinDelete,
    SkinNotExists,
    TryLater,
    isresponse,
)
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
     
     
     
     async def steam_paginate(
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
     
     
     async def inventory_skin(
          self,
          session: AsyncSession,
          skin_name: str
     ) -> Skin | AnyResponse:
          skin = await self.skin_repository.read(
               session=session,
               name=skin_name
          )
          if skin is None:
               return TryLater
          return skin
          
     
     async def inventory_paginate(
          self,
          callback_data: Paginate,
          user: User
     ) -> Paginate | AnyResponse:
          pages = ceil(len(user.skins) / 5)
          if callback_data.all_pages != pages:
               callback_data.all_pages = pages
               callback_data.offset = 0
               callback_data.current_page = 1
               return callback_data
               
          if "left" in callback_data.mode:
               callback_data.offset = callback_data.offset - 5
               callback_data.current_page = callback_data.current_page - 1
               
          elif "right" in callback_data.mode:
               callback_data.offset = callback_data.offset + 5
               callback_data.current_page = callback_data.current_page + 1
          return callback_data
     
     
     async def inventory_skin_delete(
          self,
          session: AsyncSession,
          user: User,
          skin_name: str
     ) -> AnyResponse:
          result = await self.user_skin_repository.delete(
               session=session,
               returning=True,
               user_id=user.id,
               skin_name=skin_name
          )
          if result is False:
               return SkinNotExists
          return SkinDelete
          
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService()