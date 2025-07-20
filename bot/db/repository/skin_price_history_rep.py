from bot.db.models import SkinPriceHistory

from .repository import Repository


class SkinPriceHistoryRepository(Repository[SkinPriceHistory]):
     model = SkinPriceHistory