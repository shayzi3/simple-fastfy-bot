from .abstract import AnyResponse


class DataUpdate(AnyResponse):
     text = "Данные успешно обновлены."     
     
     
class SkinCreate(AnyResponse):
     text = "Скин {} успешно добавлен."