from typing import Any, Generic, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Base
from bot.logging_ import logging_

SQLMODEL = TypeVar("SQLMODEL", bound=Base)



class Repository(Generic[SQLMODEL]):
     model: SQLMODEL
     
     
     @classmethod
     async def read(
          cls, 
          session: AsyncSession,
          with_relation: bool = False,
          all: bool = False,
          values: list[Any] = [],
          **read_where
     ) -> SQLMODEL | list[SQLMODEL] | None | list[Any]:
          sttm = (
               select(cls.model).
               filter_by(**read_where).
               order_by(cls.model.order_by())
          )
          if values:
               sttm = (
                    select(*values).
                    filter_by(**read_where).
                    order_by(cls.model.order_by())
               )
               
          if with_relation is True:
               sttm = sttm.options(*cls.model.selectinload())
          
          result = await session.execute(sttm)
          model = result.scalar() if all is False else result.scalars().all()
          logging_.db.info(f"GET DATA FROM {cls.model.__tablename__} WHERE {read_where}")
          return None if not model else model
                         
     
     @classmethod
     async def create(
          cls, 
          session: AsyncSession,
          values: dict[str, Any] | list[dict[str, Any]],
          returning: bool = True
     ) -> bool:
          sttm = (
               insert(cls.model).
               values(values)
          )
          
          if returning is True:
               sttm = sttm.returning(cls.model.returning())
               
          result = await session.execute(sttm)
          if returning is True:
               result = result.scalar()
          await session.commit()
          
          logging_.db.info(f"INSERT INTO {cls.model.__tablename__} DATA {values}")
          if returning is True:
               value = False if not result else True
               return value
               
     
     @classmethod
     async def update(
          cls, 
          session: AsyncSession,
          values: dict[str, Any],
          returning: bool = True,
          **update_where
     ) -> bool | None:
          sttm = (
               update(cls.model).
               filter_by(**update_where).
               values(values)
          )
          if returning is True:
               sttm = sttm.returning(cls.model.returning())
               
          result = await session.execute(sttm)
          if returning is True:
               result = result.scalar()
          await session.commit()
          
          logging_.db.info(f"UPDATE {cls.model.__tablename__} WHERE {update_where} DATA {values}")
          if returning is True:
               value = False if not result else True
               return value
     
     
     @classmethod
     async def delete(
          cls, 
          session: AsyncSession,
          returning: bool = True,
          **delete_where
     ) -> bool | None:
          sttm = (
               delete(cls.model).
               filter_by(**delete_where)
          )
          if returning is True:
               sttm = sttm.returning(cls.model.returning())
               
          result = await session.execute(sttm)
          if returning is True:
               result = result.scalar()
          await session.commit()
          
          logging_.db.info(f"DELETE {cls.model.__tablename__} WHERE {delete_where}")
          if returning is True:
               value = False if not result else True
               return value