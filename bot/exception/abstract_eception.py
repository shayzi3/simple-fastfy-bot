from typing import Protocol



class AbstractBotExeption(Protocol):
     
     
     @classmethod
     async def send_notify(cls, msg: str) -> None:
          ...