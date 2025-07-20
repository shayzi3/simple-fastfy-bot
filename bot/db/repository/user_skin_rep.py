from bot.db.models import UserSkin

from .repository import Repository


class UserSkinRepository(Repository[UserSkin]):
     model = UserSkin