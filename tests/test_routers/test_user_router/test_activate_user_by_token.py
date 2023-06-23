from datetime import datetime, timedelta

from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select

from models.UserModel import UserModel
from services.async_database import async_database

url = '/api/users/activate/'
access_token = AuthJWT().create_access_token(subject='user')
refresh_token = AuthJWT().create_refresh_token(subject='user')
activate_token = AuthJWT()._create_token(**{
    'subject': 2,
    'exp_time': datetime.utcnow() + timedelta(days=1),
    'type_token': 'activate',
})


async def test_When_PostForActivateUser_Should_ErrorWith405(client):
    response = await client.post(f'{url}qwer/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForActivateUser_Should_ErrorWith405(client):
    response = await client.put(f'{url}qwer/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForActivateUser_Should_ErrorWith405(client):
    response = await client.patch(f'{url}qwer/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForActivateUser_Should_ErrorWith405(client):
    response = await client.delete(f'{url}qwer/')

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForActivateUserWithRandomToken_Should_ErrorWith403(
        client):
    response = await client.get(f'{url}qwer/')

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    expected_data = {
        'detail': 'Not enough segments',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForActivateUserWithAccessToken_Should_ErrorWith403(
        client):
    response = await client.get(f'{url}{access_token}/')

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    expected_data = {
        'detail': 'Not valid token type.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForActivateUserWithRefreshToken_Should_ErrorWith403(
        client):
    response = await client.get(f'{url}{refresh_token}/')

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    expected_data = {
        'detail': 'Not valid token type.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForActivateUserWithActivateToken_Should_DataWith200(
        client, filling_users,
):
    response = await client.get(f'{url}{activate_token}/')

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'detail': 'User is activated.',
    }
    real_data = response.json()

    async with async_database.session() as db, db.begin():
        select_rows = await db.execute(
            select(
                UserModel.is_active
            ).where(
                UserModel.id == 2
            )
        )
        select_result = select_rows.scalars().first()

    expected_is_active = True
    real_is_active = select_result

    assert expected_status == real_status
    assert expected_data == real_data
    assert expected_is_active == real_is_active
