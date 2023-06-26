from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class AsyncDatabase:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init_db(self, url: str):
        self._engine = create_async_engine(url)
        self._sessionmaker = async_sessionmaker(autocommit=False,
                                                bind=self._engine)

    async def close(self):
        assert self._engine is not None, 'Database is not initialized'

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        assert self._engine is not None, 'Database is not initialized'

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        assert self._sessionmaker is not None, 'Database is not initialized'

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(BASE.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(BASE.metadata.drop_all)


async_database = AsyncDatabase()


async def get_db():
    async with async_database.session() as session, session.begin():
        yield session
