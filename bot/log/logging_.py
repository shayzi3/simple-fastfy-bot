import logging
import pytz

from datetime import datetime



class MoscowTimezone(logging.Formatter):
     moscow_tz = pytz.timezone('Europe/Moscow')
     
     def converter(self, timestamp):
          return datetime.fromtimestamp(timestamp, self.moscow_tz)

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
               filename=path + datetime.now().strftime("%Y-%m-%d") + ".txt",
          )
          format = MoscowTimezone("%(name)s %(asctime)s %(levelname)s %(message)s")
          
          logger_handler.setFormatter(format)
          self.addHandler(logger_handler)
     
     
     
class Logger:
     
     @property
     def bot(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/bot/"
          )
          
     @property
     def db(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/db/"
          )
     
     @property
     def worker(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/worker/"
          )
          
     @property
     def http_webhook(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/http/worker/"
          )
          
     @property
     def http_steam(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/http/steam/"
          )
          
     @property
     def json(self) -> BaseLogger:
          return BaseLogger(
               path="/data/logs/json/"
          )
          
          
logging_ = Logger()