from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import insert

from models.BillingAccountModel import BillingAccountModel
from models.UserModel import UserModel
from services.async_database import async_database
from services.security import security

url = '/api/billing_accounts/'
token_admin = AuthJWT().create_access_token(subject='admin')
token_user = AuthJWT().create_access_token(subject='user')


async def filling_database() -> None:
    async with async_database.session() as db, db.begin():
        await db.execute(
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
            ])
        )
        await db.execute(
            insert(
                BillingAccountModel
            ).values([
                {
                    'id': 1,
                    'balance': 1_000,
                    'user_id': 1,
                },
                {
                    'id': 2,
                    'balance': 100,
                    'user_id': 2,
                },
            ])
        )


async def test_When_PostForListBillingAccounts_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForListBillingAccounts_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForListBillingAccounts_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForListBillingAccounts_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListBillingAccountsWithOutAuth_Should_ErrorWith403(
        client):
    response = await client.get(url)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListBillAccsWithAuthUser_Should_OnlyByOwnerWith200(
        client):
    await filling_database()

    response = await client.get(**{
        'url': url,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'items': [
            {
                'id': 2,
                'balance': 100.0,
                'user_id': 2,
            },
        ],
        'next_page': None,
        'previous_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForListBillAccsWithAuthAdmin_Should_AllDataWith200(
        client):
    await filling_database()

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
                'balance': 1000.0,
                'user_id': 1,
            },
            {
                'id': 2,
                'balance': 100.0,
                'user_id': 2,
            },
        ],
        'next_page': None,
        'previous_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForListBillAccsWithAdminAndFilter_Should_DataWith200(
        client):
    await filling_database()

    response = await client.get(**{
        'url': f'{url}?user=1',
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
                'balance': 1000.0,
                'user_id': 1,
            },
        ],
        'next_page': None,
        'previous_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data
