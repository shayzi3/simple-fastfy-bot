from bot.utils.filter.callback import InventoryPaginateCallbackData
from bot.core.gen import generate_skin_id
from bot.http.steam import SteamHttpClient
from bot.db.repository import UserRepository, SkinRepository
from bot.schemas import UserDataclass



class CallbackService:
     def __init__(
          self, 
          user_repository: UserRepository,
          skin_repository: SkinRepository,
          http_client: SteamHttpClient
     ):
          self.user_repository = user_repository
          self.skin_repository = skin_repository
          self.http_client = http_client
          
          
     async def settings_notify(
          self,
          user: UserDataclass
     ) -> bool:
          update_data = {
               "notify": True if user.notify is False else False
          }
          await self.user_repository.update(
               where=user.where,
               values=update_data
          )
          return update_data.get("notify")
     
     
     async def steam_item(
          self,
          user: UserDataclass,
          item: str
     ) -> bool:
          if len(user.skins) >= 20:
               return "Максимальное кол-во предметов в инвентаре 20!"
          
          for skin in user.skins:
               if skin.name == item:
                    return "Такой предмет уже есть в вашем инвентаре."
               
          item_price = await self.http_client.item_price(item=item)
          if item_price is None:
               return "Повторите попытку позже."
          
          await self.skin_repository.create(
               values={
                    "skin_id": await generate_skin_id(),
                    "name": item,
                    "current_price": item_price,
                    "owner": user.telegram_id
               }
          )
          return "Предмет успешно добавлен в инвентарь."
     
     
     async def inventory_item(
          self,
          user: UserDataclass,
          item: str
     ) -> None:
          result = await self.skin_repository.delete(
               where={"owner": user.telegram_id, "name": item}
          )
          if result is False:
               return "Предмет в инвентаре не найден."
          return "Предмет успешно удалён."
          
     
     
     
async def get_callback_service() -> CallbackService:
     return CallbackService(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          http_client=SteamHttpClient()
     )