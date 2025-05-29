from dataclasses import dataclass
from datetime import datetime

from .base import BaseSkinDataclass, BaseUserDataclass, FromOrm, Time


@dataclass
class UserDataclass(FromOrm["UserDataclass"]):
     telegram_id: int
     created_at: datetime
     notify: bool
     update_time: Time
     skins: list[BaseSkinDataclass]
     
     
     def __post_init__(self) -> None:
          if self.skins:
               if isinstance(self.skins[0], BaseSkinDataclass) is False:
                    self.skins = [BaseSkinDataclass.from_dict(obj.__dict__) for obj in self.skins]
                    
          if isinstance(self.update_time, str) is True:
               self.update_time = Time.from_str(self.update_time)
               
               
     @property
     def where(self) -> dict[str, int]:
          return {"telegram_id": self.telegram_id}
     
     
     def sorted_skin_by_6(self) -> list[list[BaseSkinDataclass]]:
          skins_by_6 = []
          left, right = 0, 6
          for _ in range((len(self.skins) // 6) + 1):
               skins = self.skins[left:right]
               
               if skins:
                    skins_by_6.append(skins)
                    
               left += 6
               right += 6
          return skins_by_6
     
     
     def get_skin(self, name: str) -> BaseSkinDataclass | None:
          for skin in self.skins:
               if skin.name == name:
                    return skin
               
               
     @property
     def skins_names(self) -> list[str]:
          return [skin.name for skin in self.skins]
     

     

@dataclass
class SkinDataclass(FromOrm["SkinDataclass"]):
     skin_id: int
     name: str
     current_price: float
     percent: int
     user: BaseUserDataclass
     price_chart: list[int]
     
     
     def __post_init__(self) -> None:
          if isinstance(self.user, BaseUserDataclass) is False:
               self.user = BaseUserDataclass.from_dict(self.user.__dict__)
               
          if isinstance(self.price_chart, str):
               self.price_chart = [float(num) for num in self.price_chart.split(",") if num]
          
          
     @property
     def where_id(self) -> dict[str, int]:
          return {"owner": self.user.telegram_id, "skin_id": self.skin_id}
     
     
     @property
     def where_name(self) -> dict[str, int | str]:
          return {"owner": self.user.telegram_id, "name": self.name}
     
     
     @property
     def price_chart_str(self) -> str:
          return ",".join(str(num) for num in self.price_chart)
     