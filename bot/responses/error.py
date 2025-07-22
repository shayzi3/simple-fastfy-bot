from .abstract import AnyResponse


class TryLater(AnyResponse):
     text = "Повторите попытку позже"
     
     

class SkinNotFound:
     text = "По запросу {} ничего не найдено"
          
          
          
class SteamUserNotFound:
     text = "Такой пользователь не найден" 


      
class InventoryLock(AnyResponse):
     text = "Инвентарь заблокирован"
     
     
     
class InvalidSteamID(AnyResponse):
     text = "Такого ID не существует"
     
     
class SkinNotExists(AnyResponse):
     text = "Такого предмета нет в инвентаре"