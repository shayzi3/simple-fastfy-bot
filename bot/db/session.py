from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import base_config


class Session:
     engine = create_async_engine(url=base_config.sql_url)
     
     @classmethod
     def async_session(cls) -> async_sessionmaker:
          return async_sessionmaker(cls.engine)
     
     
async def async_db_session():
     async with Session.async_session()() as as_session:
          try:
               yield as_session
          finally:
               await as_session.close()