import json
import random

import aiofiles
import aiohttp
import httpx

from bot.core.config import base_config
from bot.exception import BotException
from bot.logs.logging_ import logging_
from bot.responses import (
    AnyResponse,
    InventoryEmpty,
    InventoryLock,
    SkinNotFound,
    TryLater,
)
from bot.schemas import SteamSkins, SteamUser


class SteamHttpClient:
     def __init__(self):
          self.base_url = "https://steamcommunity.com"
          
          
     @staticmethod
     async def __fake_user_agent() -> str:
          async with aiofiles.open("bot/http/steam/user_agents.txt", "r") as file:
               agents: list[str] = json.loads(await file.read())
               return random.choice(agents)
          
          
          
     async def _get_headers(self) -> dict[str, str]:
          return {"User-Agent": await self.__fake_user_agent()}
     
     
     
     async def steam_user(self, steam_id: int) -> SteamUser | AnyResponse:
          url = (
               "http://api.steampowered.com/"
               "ISteamUser/GetPlayerSummaries/v0002/"
               f"?key={base_config.steam_token}&steamids={steam_id}"
          )
          headers = await self._get_headers()
          async with aiohttp.ClientSession(headers=headers) as session:
               try:
                    async with session.get(url=url) as response:
                         if response.status != 200:
                              logging_.http_steam.error(f"SEARCH user. Status code: {response.status}. Text: {await response.text()}")
                              return TryLater
                              
                         data = await response.json()
                         return SteamUser.validate(data)
               except Exception as ex:
                    logging_.http_steam.error(f"SEARCH user {steam_id}", exc_info=ex)
                    return TryLater
          
          
     async def skin_search(
          self,
          query: str
     ) -> AnyResponse | SteamSkins:
          url = f"https://steamfolio.com/api/Popular/sort?type=2&searchTerm={query}&page=1"
          headers = await self._get_headers()
          async with aiohttp.ClientSession(headers=headers) as session:
               try:
                    async with session.get(url=url) as response:
                         if response.status != 200:
                              logging_.http_steam.error(f"SEARCH skin {query}. Code: {response.status}. Text: {await response.text()}")
                              return TryLater

                         data = await response.json()
                         pages = data["data"]["pages"]
                         skins = data["data"]["items"]
                         if not skins:
                              return SkinNotFound
                    return SteamSkins.validate(
                         pages=pages,
                         obj=skins
                    )
               except Exception as ex:
                    logging_.http_steam.error("", exc_info=ex)
                    return TryLater
          
          
     async def item_price(
          self,
          item: str
     ) -> float | None:
          item = item.replace("&", "%26")
          url = (
               self.base_url + f"/market/priceoverview/?currency=5&appid=730&market_hash_name={item}"
          )
          headers = await self._get_headers()
          async with httpx.AsyncClient(headers=headers) as session:
               logging_.http_steam.info(f"GET REQUEST STEAM FOR SEARCH PRICE ITEM: {item}")
               for _ in range(3):
                    try:
                         response = await session.get(url=url)
                         break
                    except httpx.ConnectTimeout:
                         continue
                    
               if response.status_code != 200:
                    await BotException.send_notify(msg=f"{response.text} STATUS: {response.status_code}")
                    logging_.http_steam.error(f"ERROR REQUEST TO STEAM FOR SEARCH PRICE ITEM: {item}")
                    return None
                    
               # 569,14 руб -> 569.14
               price = response.json().get("lowest_price")
               if price is None:
                    price = response.json().get("median_price")
                    if price is None:
                         logging_.http_steam.info(f"NOT FOUND PRICE: {url}")
                         return None
                    
               price = price.replace(",", ".").split()[0]
               return round(float(price), 2)
          
          
     async def inventory_by_steamid(
          self,
          steamid: int
     ) -> AnyResponse | list[str]:
          url = (
               self.base_url + f"/inventory/{steamid}/730/2"
          )
          headers = await self._get_headers()
          async with httpx.AsyncClient(headers=headers) as session:
               logging_.http_steam.info(f"GET REQUEST TO STEAM FOR FIND INVENTORY BY {steamid}")
               for _ in range(3):
                    try:
                         response = await session.get(url=url)
                         break
                    except httpx.ConnectTimeout:
                         continue
               
               if response.status_code == 403:
                    return InventoryLock
               
               if response.status_code == 401:
                    return InventoryEmpty
               
               result = response.json()
               skins = set()
               for skin in result.get("descriptions"):
                    skin_name = skin.get("market_hash_name")
                    if skin.get("tradable") == 1:
                         skins.add(skin_name)
               return list(skins)