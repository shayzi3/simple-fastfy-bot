import asyncio

from aiogram.types.bot_command import BotCommand
from aiogram_tool.depend import setup_depend_tool
from aiogram_tool.limit import setup_limit_tool

from bot.alert import Alert
from bot.core.bot import bot, dp
from bot.handlers import __routers__
from bot.middleware import __middlewares__
from bot.utils.limit_callback import callback
from bot.worker.update_check_skin_price import UpdateCheckSkinPriceWorker
from bot.worker.update_price_at_days import UpdatePriceAtDaysWorker


@dp.startup()
async def startup() -> None:
     update_check_price_worker = UpdateCheckSkinPriceWorker()
     update_price_at_days_worker = UpdatePriceAtDaysWorker()
     
     await update_check_price_worker.run()
     await update_price_at_days_worker.run()
     
     dp.include_routers(*__routers__)
     for middleware in __middlewares__:
          for event in dp.resolve_used_update_types():
               observer = dp.observers.get(event)
               observer.middleware(middleware())
              
     setup_depend_tool(dispatcher=dp)
     setup_limit_tool(dispatcher=dp, answer_callback=callback)  
          
     await bot.set_my_commands(
          [
               BotCommand(command="/start", description="Приветственное сообщение"),
               BotCommand(command="/settings", description="Пользовательские настройки"),
               BotCommand(command="/skin_search", description="Поиск предметов на Steam"),
               BotCommand(command="/inventory", description="Инвентарь"),
               BotCommand(command="/skip", description="Пропуск события"),
               BotCommand(command="/help", description="Помощь"),
               BotCommand(command="/skins_from_steam", description="Добавить предметы из Steam в инвентарь")
          ]
     )
     await Alert.notify(f"bot started")
     
     
     
@dp.shutdown()
async def shutdown() -> None:
     await Alert.notify("bot shutdown")
     

async def main() -> None:
     await dp.start_polling(bot)
     

if __name__ == "__main__":
     asyncio.run(main())
