from bot.db.models import User

from .repository import Repository


class UserRepository(Repository[User]):
     model = User