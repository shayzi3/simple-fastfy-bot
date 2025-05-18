from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.schemas import UserDataclass
from .service import CommandService


command_router = Router(name="command_router")


@command_router.message(CommandStart())
async def start(
     message: Message,
     user: UserDataclass,
     service: CommandService
):
     if user is None:
          await service.start(telegram_id=message.from_user.id)
     await message.answer("Я - бот, который поможет тебе отслеживать цены предметов CS2.")