import aiofiles
import json

from bot.log.logging_ import logging_


class JsonStorage:
     def __init__(self):
          self.path = "/data/worker.json"
          
          
     async def _get_data(self) -> list[str]:
          async with aiofiles.open(self.path, "r") as file:
               read = await file.read()
               data: list[str] = json.loads(read)
          return data
     
     
     async def run(self) -> None:
          try:
               await self._get_data()
               return None
          except:
               async with aiofiles.open("/data/worker.json", "w") as file:
                    await file.write(json.dumps([]))
          
     
     async def get(self, search_string: str) -> str | None:
          data = await self._get_data()
          logging_.json.info(f"GET VALUE: {search_string}")
          for item in data:
               if search_string is item:
                    return item
          return None
          
          
     async def get_all(self) -> list[str]:
          logging_.json.info("GET ALL DATA")
          return await self._get_data()
          
          
     async def update(self, search_string: str, new_value: str) -> None:
          data = await self._get_data()
          for index, item in enumerate(data):
               if search_string in item:
                    data.pop(index)
                    data.insert(index, new_value)
                    
          async with aiofiles.open(self.path, "w") as file:
               await file.write(json.dumps(data, indent=2))
               
          logging_.json.info(f"UPDATE DATA BY {search_string}")
               
               
     async def add(self, new_value: str) -> None:
          data = await self._get_data()
          data.append(new_value)
          
          async with aiofiles.open(self.path, "w") as file:
               await file.write(json.dumps(data, indent=2))
               
          logging_.json.info(f"ADD NEW VALUE: {new_value}")
               
               
     async def delete(self, search_string: str) -> None:
          data = await self._get_data()
          for index, item in enumerate(data):
               if search_string in item:
                    data.pop(index)
          
          async with aiofiles.open(self.path, "w") as file:
               await file.write(json.dumps(data, indent=2))
               
          logging_.json.info(f"DELETE VALUE BY: {search_string}")
          