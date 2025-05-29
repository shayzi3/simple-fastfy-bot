from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Generic

from bot.types import DATACLASS


class FromOrm(Generic[DATACLASS]):
     
     @classmethod
     def from_dict(cls, obj: dict[str, Any]) -> DATACLASS:
          return cls(
               **{key: value for key, value in obj.items() if key in cls.__dataclass_fields__}
          )
     
          
@dataclass 
class TimeOut:
     time: timedelta
     msg: str
     
     
@dataclass
class SteamUser(FromOrm["SteamUser"]):
     personaname: str
     avatarmedium: str
     profileurl: str
     


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
               return "Недопустимое время! day-hour-minute"
          
          try:
               day = int(split_obj[0])
               hour = int(split_obj[1])
               minute = int(split_obj[2])
          except ValueError:
               return "Недопустимое время! day-hour-minute"
          
          if any([day > 5, hour > 24, minute > 60]):
               return "day <= 5; hour <= 24; minute <= 60"
          
          if any([day < 0, hour < 0, minute < 0]):
               return "day >= 0; hour >= 0; minute >= 0"
          
          if (day == 0) and (hour == 0):
               if minute < 25:
                    return "day = 0; hour = 0; 25 <= minute <= 60"
          return cls(days=day, hours=hour, minutes=minute)
          
          
     @property
     def pretty_string(self) -> str:
          # -> 25m
          return " ".join([f"{value}{key[0]}" for key, value in self.__dict__.items() if value != 0])
     
     
     @property
     def to_string(self) -> str:
          return f"{self.days}-{self.hours}-{self.minutes}"
     
     
     def to_timedelta(self) -> timedelta:
          return timedelta(**self.__dict__)
          
          
          

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
     current_price: float
     percent: int
     owner: int
     price_chart: list[int]
     
     
     def __post_init__(self) -> None:
          if isinstance(self.price_chart, str):
               self.price_chart = [float(num) for num in self.price_chart.split(",") if num]
               
     
     @property
     def price_chart_str(self) -> str:
          return ",".join(str(num) for num in self.price_chart)
     
     