from datetime import datetime

from sqlalchemy import UUID, BigInteger, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload

from bot.schemas import SkinUpdateMode

from .base import Base


class User(Base):
     __tablename__ = "users"
     __table_args__ = (
          Index("idx_user_steam_id", "steam_id"),
     )
     
     id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
     name: Mapped[str] = mapped_column()
     steam_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
     steam_name: Mapped[str] = mapped_column(nullable=True)
     steam_avatar: Mapped[str] = mapped_column(nullable=True)
     steam_profile_link: Mapped[str] = mapped_column(nullable=True)
     skin_percent: Mapped[int] = mapped_column(default=10)
     created_at: Mapped[datetime] = mapped_column(server_default=func.now())
     
     skins: Mapped[list["UserSkin"]] = relationship(
          uselist=True,
          cascade="all, delete-orphan",
          back_populates="user"
     )
     
     @classmethod
     def selectinload(cls):
          return (cls.skins,)
     
     @classmethod
     def returning(cls):
          return cls.id
  
  
     
class Skin(Base):
     __tablename__ = "skins"
     
     name: Mapped[str] = mapped_column(primary_key=True)
     price: Mapped[float] = mapped_column(nullable=True)
     price_at_1_day: Mapped[float] = mapped_column(nullable=True)
     price_at_7_day: Mapped[float] = mapped_column(nullable=True)
     price_at_30_day: Mapped[float] = mapped_column(nullable=True)  
     update_mode: Mapped[SkinUpdateMode] = mapped_column(default=SkinUpdateMode.HIGH)
     
     @classmethod
     def returning(cls):
          return cls.name
    
     
     
class SkinPriceHistory(Base):
     __tablename__ = "skins_price_history"
     __table_args__ = (
          Index("idx_skin_price_history_name", "skin_name"),
          Index("idx_skin_price_history_timestamp", "timestamp")
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     price: Mapped[float] = mapped_column()
     volume: Mapped[int] = mapped_column()
     timestamp: Mapped[datetime] = mapped_column(server_default=func.now())
     
     @classmethod
     def returning(cls):
          return cls.uuid
     
     
     
class UserSkin(Base):
     __tablename__ = "users_skins"
     __table_args__ = (
          Index("idx_skin_at_user_id", "user_id"),
          Index("idx_skin_at_user_name", "skin_name"),
     )
     
     uuid: Mapped[str] = mapped_column(UUID(), primary_key=True)
     user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
     skin_name: Mapped[str] = mapped_column(ForeignKey("skins.name", ondelete="CASCADE"))
     
     skin: Mapped["Skin"] = relationship()
     user: Mapped["User"] = relationship(back_populates="skins")
     
     @classmethod
     def selectinload(cls):
          return (selectinload(cls.skin), selectinload(cls.user),)
     
     @classmethod
     def returning(cls):
          return cls.uuid