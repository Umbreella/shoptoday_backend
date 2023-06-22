from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from services.async_database import async_database
from settings import settings

from .exception_handlers import add_exception_handlers
from .routers import add_routers


def get_asgi_application(skip_init_db=False):
    lifespan = None

    if not skip_init_db:
        pg_host = settings.DATABASE_URL_HOST
        pg_port = settings.DATABASE_URL_PORT
        pg_user = settings.DATABASE_URL_USER
        pg_password = settings.DATABASE_URL_PASSWORD
        pg_db = settings.DATABASE_URL_DB

        connection_str = ''.join((
            'postgresql+psycopg://',
            f'{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}',
        ))

        async_database.init_db(connection_str)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if async_database._engine is not None:
                await async_database.close()

    app = FastAPI(**{
        'debug': True,
        'lifespan': lifespan,
    })

    add_routers(app)
    add_exception_handlers(app)

    return add_pagination(app)
