from bs4 import BeautifulSoup

from bot.logs.logging_ import logging_
from bot.utils.responses import AnyResponse, NoFoundMessage, TryLater

from .http_client import SteamHttpClient


class SteamParseClient:
     def __init__(self):
          self.http_client = SteamHttpClient()
      
     
     async def search_item(
          self,
          item: str,
     ) -> AnyResponse:
          html_text = await self.http_client.search_item(item=item)
          if html_text is None:
               return TryLater
          
          soup = BeautifulSoup(html_text, "lxml")
          content = soup.find("div", id="mainContents")
          search_result = content.find("div", id="searchResultsRows")
          no_found_message = search_result.find("div", class_="market_listing_table_message")
          
          if no_found_message is not None:
               return NoFoundMessage(no_found_message.text)
          
          return_names = []
          items = search_result.find_all("a", class_="market_listing_row_link")
          for index, item_name in enumerate(items):
               name = item_name.find("div", id=f"result_{index}").get("data-hash-name")
               return_names.append(name)
          
          logging_.http_steam.info(f"PARSE STEAM ITEMS: {item}")
          return return_names
          
          
          