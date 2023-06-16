from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from settings import settings

BASE = declarative_base()

ENGINE = create_async_engine(settings.DATABASE_URL_ASYNC)

AsyncSessionMaker = async_sessionmaker(autocommit=False, autoflush=False,
                                       bind=ENGINE, class_=AsyncSession)


async def get_db():
    async with AsyncSessionMaker() as session, session.begin():
        yield session
