from bot.db.models import Skin

from .repository import Repository


class SkinRepository(Repository[Skin]):
     model = Skin