from .abstract import AnyResponse


class DataUpdate(AnyResponse):
     text = "Данные обновлены"     
     
     
class SkinCreate(AnyResponse):
     text = "Скин {} добавлен"
     
     
class SkinDelete(AnyResponse):
     text = "Скин {} удалён"