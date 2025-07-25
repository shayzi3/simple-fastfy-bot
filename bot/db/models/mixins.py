from sqlalchemy.orm import selectinload


class UserMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          
     @classmethod
     def selectinload(cls):
          return (selectinload(cls.skins),)
     
     @classmethod
     def returning(cls):
          return cls.id
     
     @classmethod
     def order_by(cls):
          return cls.id
     
     
     
class SkinMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
     
     @classmethod
     def returning(cls):
          return cls.name
     
     @classmethod
     def order_by(cls):
          return cls.name
     
     
     
class SkinPriceHistoryMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.timestamp
     
     
     
class UserSkinMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
     
     @classmethod
     def selectinload(cls):
          return (selectinload(cls.skin), selectinload(cls.user),)
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.skin_name
     
     def skin_info(self) -> str:
          return (
               f"{self.skin_name}\n"
               f"*Price now:* {self.price}\n"
               f"*price_at_1_day:* {self.skin.price_at_1_day}\n"
               f"*price_at_7_day:* {self.skin.price_at_7_day}\n"
               f"*price_at_30_day:* {self.skin.price_at_30_day}"
          )