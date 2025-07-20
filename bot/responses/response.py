from .abstract import AnyResponse


class TryLater(AnyResponse):
     text = "Повторите попытку позже."
     
     
     
class NoFoundMessage(AnyResponse):
     def __init__(self, text: str):
          self.text = text
          
          
class InventoryLock(AnyResponse):
     text = "Инвентарь заблокирован"
     
     
     
class InventoryEmpty(AnyResponse):
     text = "Инвентарь пуст"


class InvalidSteamID(AnyResponse):
     text = "Такого ID не существует"



class InventoryLimit(AnyResponse):
     text = "Скинов не может быть больше 30!"



def isresponse(obj: type) -> bool:
     return isinstance(obj, type) and AnyResponse in obj.mro()


