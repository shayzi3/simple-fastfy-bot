import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Skin, User, UserSkin
from bot.db.repository import SkinRepository, UserRepository, UserSkinRepository
from bot.infrastracture.http.steam import SteamHttpClient
from bot.responses import (
    AnyResponse,
    InvenotoryEmpty,
    SteamSkinsExistsInInventory,
    isresponse,
)


class CommandService:
     def __init__(
          self,
          user_repository: UserRepository
     ):
          self.user_repository = user_repository
          self.skin_repository = SkinRepository
          self.user_skin_repository = UserSkinRepository
          self.http_client = SteamHttpClient()
          

     async def skins_from_steam(
          self, 
          user: User,
          session: AsyncSession
     ) -> AnyResponse | str:
          steam_skins = await self.http_client.user_inventory(
               steam_id=user.steam_id
          )
          if isresponse(steam_skins):
               return steam_skins
          
          select_data = [] 
          skin_not_found_at_user = []
          users_skin_names = [item.skin_name for item in user.skins]
          for skin in steam_skins:
               if skin not in users_skin_names:
                    select_data.append(Skin.name == skin)
                    skin_not_found_at_user.append(skin)
          
          if not skin_not_found_at_user:
               return SteamSkinsExistsInInventory
          
          skin_exists_in_table_skins = await self.skin_repository.read_all_with_or(
               session=session,
               read_data=select_data,
               values=[Skin.name]
          )
          create_skins_in_table_skins = []
          for skin in skin_not_found_at_user:
               if skin not in skin_exists_in_table_skins:
                    create_skins_in_table_skins.append({"name": skin})
                    
          if create_skins_in_table_skins:
               await self.skin_repository.create(
                    session=session,
                    values=create_skins_in_table_skins,
                    returning=False
               )
               
          create_skins_at_user = []
          for skin in skin_not_found_at_user:
               create_skins_at_user.append(
                    {
                         "uuid": uuid.uuid4(),
                         "skin_name": skin,
                         "user_id": user.id
                    }
               )
          await self.user_skin_repository.create(
               session=session,
               values=create_skins_at_user,
               returning=False
          )
          return "\n".join(skin_not_found_at_user)
     
     
     async def inventory(
          self,
          user: User,
          session: AsyncSession
     ) -> list[UserSkin] | AnyResponse:
          skins = await self.user_skin_repository.read(
               session=session,
               all=True,
               user_id=user.id
          )
          if not skins:
               return InvenotoryEmpty
          return skins
          
          
                    
          
                    
          
               
          
               
     
     
     
     
async def get_command_service() -> CommandService:
     return CommandService(
          user_repository=UserRepository
     )