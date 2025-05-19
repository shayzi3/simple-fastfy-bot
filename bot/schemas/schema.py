from datetime import datetime
from dataclasses import dataclass
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
     

     

@dataclass
class SkinDataclass(FromOrm["SkinDataclass"]):
     skin_id: int
     name: str
     image: str
     current_price: float
     user: BaseUserDataclass
     
     
     def __post_init__(self) -> None:
          if isinstance(self.user, BaseUserDataclass) is False:
               self.user = BaseUserDataclass.from_dict(self.user.__dict__)
          
          
     @property
     def where_id(self) -> dict[str, int]:
          return {"owner": self.user.telegram_id, "skin_id": self.skin_id}
     
     
     @property
     def where_name(self) -> dict[str, int | str]:
          return {"owner": self.user.telegram_id, "name": self.name}
     