import os

from dotenv import load_dotenv
from pydantic import BaseModel

from bot.constant import TEST_MODE

path = None
if TEST_MODE is True:
     path = "bot/core/test.env"
 
 
load_dotenv(dotenv_path=path)
 

class BaseConfig(BaseModel):
     bot_token: str = os.environ["BOT_TOKEN"]
     sql_url: str = os.environ["SQL_URL"]
     prod_sql_url: str = os.environ.get("PROD_SQL_URL")
     steam_token: str = os.environ["STEAM_TOKEN"]
     alert_channel: str = os.environ["ALERT_CHANNEL"]
     webhook_secret_token: str = os.environ["WEBHOOK_SECRET_TOKEN"]
     webhook: str = os.environ["WEBHOOK"]
     
     
     @property
     def webhook_full_path(self) -> str:
          return self.webhook + "/webhook/telegram/bot"
     
     
base_config = BaseConfig()