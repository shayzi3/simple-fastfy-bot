from fastapi import HTTPException, Request

from bot.core.config import base_config


async def check_secret_token(request: Request):
     token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
     if token:
          if token != base_config.webhook_secret_token:
               raise HTTPException(status_code=401)
     else:
          raise HTTPException(status_code=401)