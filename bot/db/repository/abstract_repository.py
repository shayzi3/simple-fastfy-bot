from typing import Any, Protocol
from bot.types import DATACLASS



class AbstractRepository(Protocol):
     model = None
     
     @classmethod
     async def create(
          cls,
          data: dict[str, Any]
     ) -> None:
          ...
          
     @classmethod
     async def read(
          cls,
          where: dict[str, Any],
          return_values: list[str] = []
     ) -> None | DATACLASS | list[Any]:
          ...
          
     @classmethod
     async def update(
          cls,
          where: dict[str, Any],
          values: dict[str, Any]
     ) -> bool:
          ...
          
     @classmethod
     async def delete(
          cls,
          where: dict[str, Any]
     ) -> bool:
          ...