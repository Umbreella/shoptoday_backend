import asyncio
from contextlib import ExitStack

import pytest
from httpx import AsyncClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.app import get_asgi_application
from services.async_database import async_database, get_db
from settings import settings


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield get_asgi_application(skip_init_db=True)


@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url='http://testserver') as c:
        yield c


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


postgresql_in_docker = factories.postgresql_noproc(**{
    'host': settings.DATABASE_URL_HOST,
    'port': settings.DATABASE_URL_PORT,
    'user': settings.DATABASE_URL_USER,
    'password': settings.DATABASE_URL_PASSWORD,
    'dbname': 'test_db',
})


@pytest.fixture(scope='session', autouse=True)
async def connection_test(postgresql_in_docker, event_loop):
    pg_host = postgresql_in_docker.host
    pg_port = postgresql_in_docker.port
    pg_user = postgresql_in_docker.user
    pg_db = postgresql_in_docker.dbname
    pg_password = postgresql_in_docker.password

    with DatabaseJanitor(**{
        'user': pg_user,
        'host': pg_host,
        'port': pg_port,
        'dbname': pg_db,
        'password': pg_password,
        'version': postgresql_in_docker.version,
    }):
        connection_str = ''.join((
            'postgresql+psycopg://',
            f'{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}',
        ))

        async_database.init_db(connection_str)
        yield
        await async_database.close()


@pytest.fixture(scope='function', autouse=True)
async def create_tables(connection_test):
    async with async_database.connect() as connection:
        await async_database.drop_all(connection)
        await async_database.create_all(connection)


@pytest.fixture(scope='function', autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with async_database.session() as session, session.begin():
            yield session

    app.dependency_overrides[get_db] = get_db_override
