from fastapi import status

from models.UserModel import UserModel
from schemas.UserSchema import UserSchemaStatus
from services.async_database import async_database

url = '/api/sign_in/'
data = {
    'username': 'user',
    'password': 'user',
}


async def test_When_GetForSignIn_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSignIn_Should_ErrorWith405(client):
    response = await client.put(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSignIn_Should_ErrorWith405(client):
    response = await client.patch(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSignIn_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForSignInUserNotFound_Should_ErrorWith401(client):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_401_UNAUTHORIZED
    real_status = response.status_code

    expected_data = {
        'detail': 'User not found.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForSignInWithNoActiveUser_Should_ErrorWith401(
        client, filling_users_with_passwords,
):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_401_UNAUTHORIZED
    real_status = response.status_code

    expected_data = {
        'detail': 'User not found.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForSignInWithActiveUser_Should_DataWith200(
        client, filling_users_with_passwords,
):
    async with async_database.session() as db, db.begin():
        await UserModel.update_status_by_id(**{
            'user_id': 2,
            'data': UserSchemaStatus(**{
                'is_active': True,
            }),
            'db': db,
        })

    response = await client.post(url, json=data)

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_keys = ('access', 'refresh',)
    real_keys = tuple(response.json().keys())

    assert expected_status == real_status
    assert expected_keys == real_keys
