from constant import TEST_MODE
from pydantic_settings import BaseSettings, SettingsConfigDict

path = "bot/core/prod.env"
if TEST_MODE is True:
     path = "bot/core/test.env"
     



class BaseConfig(BaseSettings):
     bot_token: str
     sql_url: str
     webhook_url: str
     webhook_token: str
     admins: list[int]
     
     @property
     def bot_webhook_url(self) -> str:
          return self.webhook_url + "/webhook/telegram"
     
     model_config = SettingsConfigDict(env_file=path)
     
     
base_config = BaseConfig()