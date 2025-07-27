import asyncio

from bot.logging_ import logging_

from .base import CheckPricesBaseWorker


class CheckPricesWorker(CheckPricesBaseWorker):
     def __init__(self):
          super().__init__()
          
          
     async def run(self) -> None:
          ...
          
          