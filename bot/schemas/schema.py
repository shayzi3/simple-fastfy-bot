from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any

from bot.responses import AnyResponse, SteamUserNotFound
from bot.utils.compress import CompressSkinName


@dataclass
class SteamUser:
     steam_id: int
     steam_name: str
     steam_avatar: str
     steam_profile_link: str
     
     
     @classmethod
     def validate(cls, obj: dict[str, Any]) -> SteamUser | AnyResponse:
          player = obj.get("response").get("players")
          if not player:
               return SteamUserNotFound
          
          steam_user = player[0]
          return cls(
               steam_id=int(steam_user.get("steamid")),
               steam_name=steam_user.get("personaname"),
               steam_avatar=steam_user.get("avatar"),
               steam_profile_link=steam_user.get("profileurl")
          )
          
         
@dataclass
class SteamSkins:
     pages: int
     skins: list[str]
     
     @classmethod
     def validate(cls, obj: list[dict[str, Any]]) -> "SteamSkins":
          return cls(
               pages=ceil(len(obj) / 5),
               skins=[
                    CompressSkinName.compress(
                         from_compress=False,
                         name=skin.get("marketHashName")
                    ) for skin in obj
               ]
          )
    
    
    
@dataclass
class NotifySkin:
     skin_name: str
     price: float
     price_percent: float
     change_price_at_day: int
     
     
     def pretty(self) -> str:
          return (
               f"Изменение цены за {self.change_price_at_day} дней в процентах: {self.price_percent}\n"
               f"Нынешняя цена: {self.price}"
          )
     
     
@dataclass
class NotifyData:
     skins: list[NotifySkin]
     
     def pretty_skins(self) -> str:
          text = f"{self.skins[0].skin_name}\n\n"
          body = "\n\n".join([skin.pretty() for skin in self.skins])
          return text + body
