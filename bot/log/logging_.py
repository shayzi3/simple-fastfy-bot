import logging

from datetime import datetime


class BaseLogger(logging.Logger):
     def __init__(self, path: str) -> None:
          super().__init__(name="LOG")
          self.setLevel(logging.DEBUG)
          
          logger_handler = logging.FileHandler(
               filename=path + datetime.now().strftime("%Y-%m-%d") + ".txt",
          )
          format = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
          
          logger_handler.setFormatter(format)
          self.addHandler(logger_handler)
     
     
     
class Logger:
     
     @property
     def bot(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/bot/"
          )
          
     @property
     def db(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/db/"
          )
     
     @property
     def worker(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/worker/"
          )
          
     @property
     def http_webhook(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/http/worker/"
          )
          
     @property
     def http_steam(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/http/steam/"
          )
          
     @property
     def json(self) -> BaseLogger:
          return BaseLogger(
               path="bot/log/logs/json/"
          )
          
          
logging_ = Logger()