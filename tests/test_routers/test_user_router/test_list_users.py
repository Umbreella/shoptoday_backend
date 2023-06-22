from typing import List

from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import insert

from models.UserModel import UserModel
from services.async_database import async_database
from services.security import security

url = '/api/users/'
token_admin = AuthJWT().create_access_token(subject='admin')
token_user = AuthJWT().create_access_token(subject='user')


async def filling_database() -> List[str]:
    async with async_database.session() as db, db.begin():
        insert_rows = await db.execute(
            insert(
                UserModel
            ).values([
                {
                    'id': 1,
                    'username': 'admin',
                    'password': security.get_password_hash('w' * 10),
                    'is_superuser': True,
                    'is_active': False,
                },
                {
                    'id': 2,
                    'username': 'user',
                    'password': security.get_password_hash('q' * 10),
                    'is_superuser': False,
                    'is_active': False,
                },
            ]).returning(UserModel.password)
        )

    return insert_rows.scalars().all()


async def test_When_PostForListUsers_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForListUsers_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForListUsers_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForListUsers_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListUsersWithOutAuthUser_Should_ErrorWith403(
        client):
    response = await client.get(url)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListUsersWithRandomAuth_Should_ErrorWith403(
        client):
    await filling_database()

    response = await client.get(**{
        'url': url,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListUsersWithAdminUser_Should_DataWith200(
        client):
    passwords = await filling_database()

    response = await client.get(**{
        'url': url,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'items': [
            {
                'id': 1,
                'is_active': False,
                'is_superuser': True,
                'username': 'admin',
                'password': passwords[0],
            },
            {
                'id': 2,
                'is_active': False,
                'is_superuser': False,
                'username': 'user',
                'password': passwords[1],
            },
        ],
        'next_page': None,
        'previous_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data
