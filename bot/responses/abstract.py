from typing import Protocol

from aiogram.types import Message


class AnyResponse(Protocol):
     text: str
     
     
     @classmethod
     async def answer(cls, message: Message) -> None:
          await message.answer(text=cls.text)
     
     
     