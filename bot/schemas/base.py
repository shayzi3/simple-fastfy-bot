from datetime import datetime
from dataclasses import dataclass
from typing import Any, Generic

from bot.types import DATACLASS



class FromOrm(Generic[DATACLASS]):
     
     @classmethod
     def from_orm(cls, obj: dict[str, Any]) -> DATACLASS:
          return cls(
               **{key: value for key, value in obj.items() if key in cls.__dataclass_fields__}
          )



@dataclass
class BaseUserDataclass(FromOrm["BaseUserDataclass"]):
     telegram_id: int
     created_at: datetime
     notify: bool
     update_time: str
     
   
     
@dataclass
class BaseSkinDataclass(FromOrm["BaseSkinDataclass"]):
     skin_id: int
     name: str
     image: str
     current_price: float
     owner: int
     
     