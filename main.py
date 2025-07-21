import asyncio

from aiogram.types.bot_command import BotCommand
from aiogram_tool.depend import setup_depend_tool
from aiogram_tool.limit import setup_limit_tool

from bot.core.bot import bot, dp
from bot.handlers import __routers__
from bot.middleware import __middlewares__


@dp.startup()
async def startup() -> None:
     # background workers
     
     setup_depend_tool(dispatcher=dp, middleware=True)
     setup_limit_tool(dispatcher=dp, answer_callback=None)
     
     dp.include_routers(*__routers__)
     for middleware in __middlewares__:
          for event in dp.resolve_used_update_types():
               observer = dp.observers.get(event)
               observer.middleware(middleware())
               
     await bot.set_my_commands(
          [
               BotCommand(command="/start", description="Приветственное сообщение"),
               BotCommand(command="/settings", description="Пользовательские настройки"),
               BotCommand(command="/skin_search", description="Поиск предметов на Steam"),
               BotCommand(command="/inventory", description="Инвентарь"),
               BotCommand(command="/skin_price_history", description="История изменения цены скина"),
               BotCommand(command="/skip", description="Пропуск события"),
               BotCommand(command="/help", description="Помощь"),
               BotCommand(command="/skins_from_steam", description="Добавить предметы из Steam в инвентарь")
          ]
     )
     
   
     
@dp.shutdown()
async def shutdown() -> None:
     pass
     
    
     
async def main() -> None:
     await dp.start_polling(bot)
     

if __name__ == "__main__":
     asyncio.run(main())
