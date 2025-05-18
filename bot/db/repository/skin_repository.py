from .repository import Repository
from bot.schemas import SkinDataclass
from bot.db.models import Skin


class SkinRepository(Repository[SkinDataclass]):
     model = Skin