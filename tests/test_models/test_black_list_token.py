import uuid

from sqlalchemy.dialects.postgresql import insert

from models.BlackListToken import BlackListToken
from services.async_database import async_database

tested_class = BlackListToken
data = {
    'jti': str(uuid.uuid4()),
    'exp': 1,
}


async def test_When_CallCheckTokenByJtiWithNotFoundJti_Should_ReturnFalse():
    async with async_database.session() as db, db.begin():
        has_token = await tested_class.check_token_by_jti(data.get('jti'), db)

    expected_has_token = False
    real_has_token = has_token

    assert expected_has_token == real_has_token


async def test_When_CallCheckTokenByJtiWithFoundJti_Should_ReturnTrue():
    async with async_database.session() as db, db.begin():
        await db.execute(
            insert(tested_class).values(data)
        )

        has_token = await tested_class.check_token_by_jti(data.get('jti'), db)

    expected_has_token = True
    real_has_token = has_token

    assert expected_has_token == real_has_token


async def test_When_CallAddInBlackList_Should_AddRowInTable():
    async with async_database.session() as db, db.begin():
        token_is_add = await tested_class.add_in_black_list(**{
            **data,
            'db': db,
        })

    expected_has_token = True
    real_has_token = token_is_add

    assert expected_has_token == real_has_token
