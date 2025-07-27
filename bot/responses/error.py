from .abstract import AnyResponse


class TryLater(AnyResponse):
     text = "Повторите попытку позже"
     
     

class SkinNotFound(AnyResponse):
     text = "По запросу {} ничего не найдено"
          
          
          
class SteamUserNotFound:
     text = "Такой пользователь не найден" 


      
class InventoryLock(AnyResponse):
     text = "Инвентарь заблокирован"
     
     
     
class InvalidSteamID(AnyResponse):
     text = "Такого ID не существует"
     
     
class SkinNotExists(AnyResponse):
     text = "Такого предмета нет в инвентаре"
     
     
class InvenotoryEmpty(AnyResponse):
     text = "Инвентарь пуст"
     
     
     
class SteamSkinsExistsInInventory(AnyResponse):
     text = "Все предметы из инвентаря Steam уже есть у вас."