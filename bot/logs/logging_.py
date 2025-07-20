import logging
from datetime import datetime

from bot.constant import TEST_MODE
from bot.core.timezone import time_now, timezone

path = "/data/logs"
if TEST_MODE is True:
     path = "data/logs"



class MoscowTimezone(logging.Formatter):
     
     def converter(self, timestamp):
          return datetime.fromtimestamp(timestamp, timezone)

     def formatTime(self, record, datefmt=None):
          dt = self.converter(record.created)
          if datefmt:
               return dt.strftime(datefmt)
          else:
               return dt.isoformat()
          
          

class BaseLogger(logging.Logger):
     def __init__(self, path: str) -> None:
          super().__init__(name="LOG")
          self.setLevel(logging.DEBUG)
          
          logger_handler = logging.FileHandler(
               filename=path + time_now().strftime("%Y-%m-%d") + ".txt",
          )
          format = MoscowTimezone("%(name)s %(asctime)s %(levelname)s %(message)s")
          
          logger_handler.setFormatter(format)
          self.addHandler(logger_handler)
     
     
     
class Logger:
     
     @property
     def bot(self) -> BaseLogger:
          return BaseLogger(
               path=path + "/bot/"
          )
          
     @property
     def db(self) -> BaseLogger:
          return BaseLogger(
               path=path + "/db/"
          )
     
     @property
     def http_webhook(self) -> BaseLogger:
          return BaseLogger(
               path=path + "/http/webhook/"
          )
          
     @property
     def http_steam(self) -> BaseLogger:
          return BaseLogger(
               path=path + "/http/steam/"
          )
          
          
logging_ = Logger()