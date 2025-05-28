from bot.db.models import User
from bot.schemas import UserDataclass

from .repository import Repository


class UserRepository(Repository[UserDataclass]):
     model = User