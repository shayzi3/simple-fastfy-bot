import httpx

from fake_useragent import UserAgent

from bot.log.logging_ import logging_
from bot.exception import BotException



class SteamHttpClient:
     def __init__(self):
          self.base_url = "https://steamcommunity.com"
          self.headers = {
               "user-agent": UserAgent().chrome
          }
          
          
     async def search_item(
          self,
          item: str
     ) -> str | None:
          url = (
               self.base_url + f"/market/search?l=russian&appid=730&q={item}"
          )
          async with httpx.AsyncClient(headers=self.headers) as session:
               response = await session.get(url=url)
               
               logging_.http_steam.info(f"GET REQUEST STEAM FOR SEARCH ITEM: {item}")
               
               if response.status_code != 200:
                    await BotException.send_notify(msg=response.text)
                    logging_.http_steam.error(f"ERROR REQUEST TO STEAM FOR SEARCH ITEM: {item}")
                    return None
               
               return response.text
          
          
     async def item_price(
          self,
          item: str
     ) -> float:
          url = (
               self.base_url + f"/market/priceoverview/?currency=5&appid=730&market_hash_name={item}"
          )
          async with httpx.AsyncClient(headers=self.headers) as session:
               response = await session.get(url=url)
               
               logging_.http_steam.info(f"GET REQUEST STEAM FOR SEARCH PRICE ITEM: {item}")
               
               if response.status_code != 200:
                    await BotException.send_notify(msg=response.text)
                    logging_.http_steam.error(f"ERROR REQUEST TO STEAM FOR SEARCH PRICE ITEM: {item}")
                    return None
               
               # 569,14 руб -> 569.14
               price = response.json().get("lowest_price")
               price = price.replace(",", ".").split()[0]
               return round(float(price), 2)
               