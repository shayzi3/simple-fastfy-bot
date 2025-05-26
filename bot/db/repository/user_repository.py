from .repository import Repository
from bot.schemas import UserDataclass
from bot.db.models import User


class UserRepository(Repository[UserDataclass]):
     model = User