from datetime import datetime

import pytz

timezone = pytz.timezone(zone="Europe/Moscow")

def time_now() -> datetime:
     return datetime.now(timezone)