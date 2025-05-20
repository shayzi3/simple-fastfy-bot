import pytz
from datetime import datetime


timezone = pytz.timezone(zone="Europe/Moscow")

def time_now() -> datetime:
     return datetime.now(timezone)