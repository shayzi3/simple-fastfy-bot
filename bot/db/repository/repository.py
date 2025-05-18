from typing import Any, Generic
from sqlalchemy import select, insert, update, delete

from bot.log.logging_ import logging_
from bot.types import DATACLASS
from bot.db.session import Session
from .abstract_repository import AbstractRepository




class Repository(AbstractRepository, Generic[DATACLASS]):
     model = None
     
     @classmethod
     async def read(
          cls, 
          where: dict[str, Any], 
          return_values: list[str] = []
     ) -> None | DATACLASS | list[Any]:
          async with Session.async_session() as session:
               logging_.db.info(f"GET DATA FROM {cls.model.__tablename__} WHERE {where}")
               
               sttm = select(cls.model).filter_by(**where)
               result = await session.execute(sttm)
               scalar = result.scalar()
               
               if not scalar:
                    return None

          if return_values:
               return [getattr(scalar, name, None) for name in return_values]
          return cls.model.dataclass_model.from_dict(scalar.__dict__)
          
          
     
     @classmethod
     async def create(
          cls, 
          values: dict[str, Any]
     ) -> None:
          async with Session.async_session() as session:
               logging_.db.info(f"INSERT DATA IN {cls.model.__tablename__} VALUE {values}")
               
               sttm = insert(cls.model).values(**values)
               await session.execute(sttm)
               await session.commit()
               
          
     
     @classmethod
     async def update(
          cls, 
          where: dict[str, Any], 
          values: dict[str, Any]
     ) -> bool:
          async with Session.async_session() as session:
               logging_.db.info(f"UPDATE DATA IN {cls.model.__tablename__} WHERE {where} VALUE {values}")
               
               sttm = (
                    update(cls.model).
                    filter_by(**where).
                    values(**values).
                    returning(cls.model.returning_value())
               )
               result = await session.execute(sttm)
               result = result.fetchone()
               
               if not result:
                    return False
               
               await session.commit()
               return True
     
     
     @classmethod
     async def delete(
          cls, 
          where: dict[str, Any]
     ) -> bool:
          async with Session.async_session() as session:
               logging_.db.info(f"DELETE DATA FROM {cls.model.__tablename__} WHERE {where}")
               
               sttm = (
                    delete(cls.model).
                    filter_by(**where).
                    returning(cls.model.returning_value())
               )
               result = await session.execute(sttm)
               result = result.fetchone()
               
               if not result:
                    return False
               
               await session.commit()
               return True