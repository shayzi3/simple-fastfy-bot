from .abstract import AnyResponse


class TryLater(AnyResponse):
     text = "Повторите попытку позже."
     
     

class SkinNotFound:
     text = "По запросу {} ничего не найдено."
          
          
          
class SteamUserNotFound:
     text = "Такой пользователь не найден." 


      
class InventoryLock(AnyResponse):
     text = "Инвентарь заблокирован."
     
     
     
class InventoryEmpty(AnyResponse):
     text = "Инвентарь пуст."



class InvalidSteamID(AnyResponse):
     text = "Такого ID не существует."