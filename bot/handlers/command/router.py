from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


command_router = Router(name="command_router")


@command_router.message(CommandStart())
async def start(message: Message):
     await message.answer("Hello!")