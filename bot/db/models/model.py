from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger, func, JSON

from bot.schemas import UserDataclass, SkinDataclass
from .base import Base




class User(Base):
     __tablename__ = "users"
     dataclass_model = UserDataclass
     
     telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
     notify: Mapped[bool] = mapped_column(default=False, nullable=False)
     update_time: Mapped[str] = mapped_column(nullable=False)
     
     skins: Mapped[list["Skin"]] = relationship(
          back_populates="user",
          lazy="joined",
          uselist=True
     )
     
     @classmethod
     def returning_value(cls):
          return cls.telegram_id
     
  
     
class Skin(Base):
     __tablename__ = "skins"
     dataclass_model = SkinDataclass
     
     skin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
     name: Mapped[str] = mapped_column(nullable=False)
     current_price: Mapped[float] = mapped_column(nullable=False)
     percent: Mapped[int] = mapped_column(nullable=False)
     price_chart: Mapped[str] = mapped_column(nullable=True)
     owner: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
     
     user: Mapped["User"] = relationship(
          back_populates="skins",
          lazy="joined"
     )
     
     @classmethod
     def returning_value(cls):
          return cls.skin_id