import uvicorn
import asyncio

from aiogram.types.bot_command import BotCommand
from fastapi import FastAPI
from contextlib import asynccontextmanager

from bot.db.repository import UserRepository, SkinRepository
from bot.http.steam import SteamHttpClient
from bot.db.json_storage import JsonStorage
from bot.worker.monitoring import MonitoringWorker
from bot.core.bot import bot, dp
from bot.core.config import base_config
from bot.http.webhook import webhook_router
from bot.middleware import __middlewares__
from bot.handlers import __routers__




@asynccontextmanager
async def lifespan(_: FastAPI):
     dp.include_routers(*__routers__)
     for middleware in __middlewares__:
          dp.message.middleware(middleware())
          dp.callback_query.middleware(middleware())
          
     json_storage = JsonStorage()
     await json_storage.run()
          
     monitoring = MonitoringWorker(
          user_repository=UserRepository,
          skin_repository=SkinRepository,
          json_storage=json_storage,
          http_client=SteamHttpClient()
     )
     asyncio.create_task(monitoring.run())
     
     await bot.set_my_commands(
          [
               BotCommand(command="/start", description="Приветственное сообщение"),
               BotCommand(command="/settings", description="Пользовательские настройки"),
               BotCommand(command="/search", description="Поиск предметов"),
               BotCommand(command="/inventory", description="Инвентарь"),
               BotCommand(command="/chart", description="Генерация графика"),
               BotCommand(command="/skip", description="Пропуск события"),
               BotCommand(command="/help", description="Помощь")
          ]
     )
     
     await bot.set_webhook(
          url=base_config.bot_webhook_url,
          secret_token=base_config.webhook_token,
          drop_pending_updates=True,
          allowed_updates=dp.resolve_used_update_types()
     )
     yield
     await bot.delete_webhook(drop_pending_updates=True)
     
     
app = FastAPI(
     title="SimpleFastFy",
     lifespan=lifespan
)
app.include_router(webhook_router)


if __name__ == "__main__":
     uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True)

