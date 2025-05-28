from fastapi import HTTPException, Request, status

from bot.core.config import base_config


async def validate_token(request: Request) -> None:
     token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
     if token != base_config.webhook_token:
          raise HTTPException(
               detail="Invalid Token!",
               status_code=status.HTTP_401_UNAUTHORIZED
          )