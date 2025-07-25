from datetime import datetime, timedelta
from math import ceil

from aiogram.types.base import TelegramObject


async def callback(
     event: TelegramObject,
     _: timedelta,
     time_last: datetime
):
     await event.answer(f"До следуюшего использования осталось: {ceil(time_last.total_seconds())} секунд")