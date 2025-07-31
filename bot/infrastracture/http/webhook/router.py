from aiogram.types import Update
from fastapi import APIRouter, Depends, Request, Response

from bot.core.bot import bot, dp

from .dependency import check_secret_token

webhook_router = APIRouter(prefix="/webhook")



@webhook_router.post(path="/telegram/bot", dependencies=[Depends(check_secret_token)])
async def telegram_bot(request: Request):
     update = Update.model_validate(await request.json(), context={"bot": bot})
     await dp.feed_update(bot=bot, update=update, dispatcher=dp)
     return Response()