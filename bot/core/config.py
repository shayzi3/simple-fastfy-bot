import os

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from bot.constant import TEST_MODE

if TEST_MODE is True:
     class BaseConfig(BaseSettings):
          bot_token: str
          sql_url: str
          steam_token: str
          alert_channel: str
          
          model_config = SettingsConfigDict(env_file="bot/core/test_env.env")
else:
     class BaseConfig(BaseModel):
          bot_token: str = os.environ["BOT_TOKEN"]
          sql_url: str = os.environ["SQL_URL"]
          steam_token: str = os.environ["STEAM_TOKEN"]
          alert_chanel: str = os.environ["ALERT_CHANNEL"]
     
     
base_config = BaseConfig()