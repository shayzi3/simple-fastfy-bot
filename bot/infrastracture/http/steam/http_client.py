import json
import random

import aiofiles
import aiohttp

from bot.core.config import base_config
from bot.logs.logging_ import logging_
from bot.responses import AnyResponse, InventoryLock, SkinNotFound, TryLater
from bot.schemas import SteamSkins, SteamUser


class SteamHttpClient:
     def __init__(self):
          self.base_url = "https://steamcommunity.com"
          
          
     @staticmethod
     async def __fake_user_agent() -> str:
          async with aiofiles.open("bot/infrastracture/http/user_agents.txt", "r") as file:
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
                    return SteamSkins.validate(obj=skins)
               except Exception as ex:
                    logging_.http_steam.error("error", exc_info=ex)
                    return TryLater
          
          
     async def user_inventory(
          self,
          steam_id: int
     ) -> AnyResponse | list[str]:
          url = (
               self.base_url + f"/inventory/{steam_id}/730/2"
          )
          headers = await self._get_headers()
          async with aiohttp.ClientSession(headers=headers) as session:
               try:
                    async with session.get(url=url) as response:
                         logging_.http_steam.info(f"GET REQUEST TO STEAM FOR FIND INVENTORY BY {steam_id}")
                         if response.status == 429:
                              return TryLater
                         
                         if response.status != 200:
                              return InventoryLock
                                        
                    data = await response.json()
                    skins = set()
                    for skin in data.get("descriptions"):
                         skin_name = skin.get("market_hash_name")
                         if skin.get("tradable") == 1:
                              skins.add(skin_name)
                    return list(skins)
               
               except Exception as ex:
                    logging_.http_steam.error("error", exc_info=ex)
                    return TryLater