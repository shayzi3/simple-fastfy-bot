from aiogram import Bot, Dispatcher
from .config import base_config


bot = Bot(token=base_config.bot_token)
dp = Dispatcher()