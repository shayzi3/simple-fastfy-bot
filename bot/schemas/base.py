from datetime import datetime
from dataclasses import dataclass
from typing import Any, Generic

from bot.types import DATACLASS



class FromOrm(Generic[DATACLASS]):
     
     @classmethod
     def from_dict(cls, obj: dict[str, Any]) -> DATACLASS:
          return cls(
               **{key: value for key, value in obj.items() if key in cls.__dataclass_fields__}
          )

@dataclass
class Time:
     days: int
     hours: int
     minutes: int


     @classmethod
     def from_str(cls, obj: str) -> "Time":
          """days-hours-minutes"""
          split_obj = obj.split("-")
          if len(split_obj) < 3:
               return "Недопустимое время! day:hour:minute"
          
          try:
               day = int(split_obj[0])
               hour = int(split_obj[1])
               minute = int(split_obj[2])
          except ValueError:
               return "Недопустимое время! day:hour:minute"
          
          if any([day > 5, hour > 24, minute > 60]):
               return "Недопустимое время! day < =5 hour <= 24 minute <= 60"
          
          if any([day < 0, hour < 0, minute < 0]):
               return "Недопустимое время! day >= 0 hour >= 0 minute >= 0"
          
          if (day == 0) and (hour == 0):
               if minute < 25:
                    return "Недопустимое время! При day = 0 и hour = 0, 25 <= minute <= 60"
          return cls(days=day, hours=hour, minutes=minute)
          
          
     @property
     def pretty_string(self) -> str:
          return f"d: {self.days} h: {self.hours} m: {self.minutes}"
     
     
     @property
     def to_string(self) -> str:
          return f"{self.days}-{self.hours}-{self.minutes}"
          
          
          

@dataclass
class BaseUserDataclass(FromOrm["BaseUserDataclass"]):
     telegram_id: int
     created_at: datetime
     notify: bool
     update_time: Time
     
     def __post_init__(self) -> None:
          if isinstance(self.update_time, str) is True:
               self.update_time = Time.from_str(self.update_time)
     
   
     
@dataclass
class BaseSkinDataclass(FromOrm["BaseSkinDataclass"]):
     skin_id: int
     name: str
     image: str
     current_price: float
     owner: int
     
     