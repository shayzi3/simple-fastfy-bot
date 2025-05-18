from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
     dataclass_model: type