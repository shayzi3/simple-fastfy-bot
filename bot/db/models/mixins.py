
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
     
     def steam_account_info(self) -> str:
          return (
               f"*Nickname:* {self.steam_name}\n"
               f"*SteamID:* {self.steam_id}\n"
               f"*Процент:* {self.skin_percent}"
          )
          
     def check_percent(self, percent: float) -> bool:
          if percent <= 0:
               percent *= -1
          return percent >= self.skin_percent
     
     
     
class SkinMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
     
     @classmethod
     def returning(cls):
          return cls.name
     
     @classmethod
     def order_by(cls):
          return cls.name
     
     @classmethod
     def selectiload(cls):
          return (selectinload(cls.price_history),)
     
     def skin_info(self) -> str:
          return (
               f"{self.name}\n"
               f"<b>Price now:</b> {self.price}\n"
               f"<b>price_at_1_day:</b> {self.price_at_1_day}\n"
               f"<b>price_at_7_day:</b> {self.price_at_7_day}\n"
               f"<b>price_at_30_day:</b> {self.price_at_30_day}"
          )
     
     
     
class SkinPriceHistoryMixin:
     def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     @classmethod
     def order_by(cls):
          return cls.timestamp
     
     @classmethod
     def selectinload(cls):
          return (selectinload(cls.skin),)
     
     
     
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