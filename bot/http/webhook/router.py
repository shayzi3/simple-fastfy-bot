from fastapi import (
     APIRouter, 
     Depends,
     Request,
     Response
)
from aiogram.types import Update

from bot.core.bot import bot, dp
from .depend import validate_token


webhook_router = APIRouter(
     prefix="/webhook",
     tags=["Webhook"],
     dependencies=[Depends(validate_token)]
)


@webhook_router.post("/telegram")
async def telegram(request: Request) -> Response:
     update = Update.model_validate(await request.json(), context={"bot": bot})
     await dp.feed_update(bot, update)
     return Response()