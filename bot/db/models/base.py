from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
     
     @classmethod
     def selectinload(cls):
          return ()
     
     @classmethod
     def returning(cls):
          pass
     
     @classmethod
     def order_by(cls):
          pass