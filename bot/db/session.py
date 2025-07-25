from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import base_config


class Session:
     engine = create_async_engine(url=base_config.sql_url)
     async_session = async_sessionmaker(engine)
     

@asynccontextmanager
async def async_db_session():
     async with Session.async_session() as as_session:
          try:
               yield as_session
          finally:
               await as_session.close()