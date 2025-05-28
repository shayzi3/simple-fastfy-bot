from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.core.config import base_config


class Session:
     engine = create_async_engine(url=base_config.sql_url)
     async_session = async_sessionmaker(engine)