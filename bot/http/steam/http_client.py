import httpx
import aiofiles
import json
import random


from bot.log.logging_ import logging_
from bot.exception import BotException



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
     
          
     async def search_item(
          self,
          item: str
     ) -> str | None:
          url = (
               self.base_url + f"/market/search?l=russian&appid=730&q={item}"
          )
          headers = await self._get_headers()
          async with httpx.AsyncClient(headers=headers) as session:
               logging_.http_steam.info(f"GET REQUEST STEAM FOR SEARCH ITEM: {item}")
               for _ in range(3):
                    try:
                         response = await session.get(url=url)
                         break
                    except httpx.ConnectTimeout:
                         continue
               
               if response.status_code != 200:
                    await BotException.send_notify(msg=response.text)
                    logging_.http_steam.error(f"ERROR REQUEST TO STEAM FOR SEARCH ITEM: {item}")
                    return None
               return response.text
          
          
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
          
               