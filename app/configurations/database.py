from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_async_engine(settings.db_dsn)


class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all


def drop_db():
    Base.metadata.drop_all
