from copy import copy

from sqlalchemy import select

from models.UserModel import UserModel
from schemas.UserSchema import UserSchemaIn, UserSchemaOut, UserSchemaStatus
from services.async_database import async_database

tested_class = UserModel
data_user = {
    'username': 'user',
    'password': 'user',
}
data_admin = {
    'username': 'admin',
    'password': 'admin',
}


async def test_When_AuthWithUserNotFound_Should_ReturnNone():
    local_data = UserSchemaIn(**data_user)

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.authenticate(local_data, db)

    expected_user = None
    real_user = user_orm

    assert expected_user == real_user


async def test_When_AuthWithUserNoActive_Should_ReturnNone(filling_users):
    local_data = UserSchemaIn(**data_user)

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.authenticate(local_data, db)

    expected_user = None
    real_user = user_orm

    assert expected_user == real_user


async def test_When_AuthActiveUserWithBadPass_Should_ReturnNone(
        filling_users_with_passwords,
):
    data = copy(data_admin)
    data.update({
        'password': 'user',
    })

    local_data = UserSchemaIn(**data)

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.authenticate(local_data, db)

    expected_user = None
    real_user = user_orm

    assert expected_user == real_user


async def test_When_AuthActiveUser_Should_ReturnNone(
        filling_users_with_passwords,
):
    local_data = UserSchemaIn(**data_admin)

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.authenticate(local_data, db)

    expected_user = None
    real_user = user_orm

    assert expected_user != real_user


async def test_When_CallGetAllQuery_Should_ReturnSelectWithOrderBy():
    expected_query = str(
        select(
            tested_class
        ).order_by(
            tested_class.id
        ))
    real_query = str(await tested_class.get_all_query())

    assert expected_query == real_query


async def test_When_CallCreate_Should_CreateNewRowInTable():
    data = UserSchemaIn(**data_user)

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.create(data, db)
        user = UserSchemaOut.from_orm(user_orm)

    expected_username = 'user'
    real_username = user.username

    expected_password = 'user'
    real_password = user.password

    expected_is_active = False
    real_is_active = user.is_active

    expected_is_superuser = False
    real_is_superuser = user.is_superuser

    assert expected_username == real_username
    assert expected_password != real_password
    assert expected_is_active == real_is_active
    assert expected_is_superuser == real_is_superuser


async def test_When_CallCreateWithDuplicateUsername_Should_DontCreateRow(
        filling_users,
):
    data = UserSchemaIn(**data_user)

    async with async_database.session() as db, db.begin():
        await tested_class.create(data, db)
        user_orm = await tested_class.create(data, db)

    expected_user_orm = None
    real_user_orm = user_orm

    assert expected_user_orm == real_user_orm


async def test_When_CallUpdateStatusById_Should_ChangeStatus(filling_users):
    data = UserSchemaStatus(**{
        'is_active': True,
    })

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.update_status_by_id(1, data, db)
        user = UserSchemaOut.from_orm(user_orm)

    expected_is_active = True
    real_is_active = user.is_active

    assert expected_is_active == real_is_active


async def test_When_CallGetByUsernameWithNotValidArgs_Should_ReturnNone():
    username = 'admin'

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.get_by_username(username, db)

    expected_user_id = None
    real_user_id = user_orm

    assert expected_user_id == real_user_id


async def test_When_CallGetByUsernameWithValidArgs_Should_ReturnUser(
        filling_users,
):
    username = 'admin'

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.get_by_username(username, db)
        user = UserSchemaOut.from_orm(user_orm)

    expected_user_id = 1
    real_user_id = user.id

    assert expected_user_id == real_user_id


async def test_When_CallGetByIdWithNotValidArgs_Should_ReturnNone():
    user_id = 1

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.get_by_id(user_id, db)

    expected_user_id = None
    real_user_id = user_orm

    assert expected_user_id == real_user_id


async def test_When_CallGetByIdWithValidArgs_Should_ReturnUser(
        filling_users,
):
    user_id = 1

    async with async_database.session() as db, db.begin():
        user_orm = await tested_class.get_by_id(user_id, db)
        user = UserSchemaOut.from_orm(user_orm)

    expected_user_id = 1
    real_user_id = user.id

    assert expected_user_id == real_user_id
