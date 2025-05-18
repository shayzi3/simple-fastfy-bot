import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

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
          dp.callback_query(middleware())
          
     # start monitoring
     
     
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

