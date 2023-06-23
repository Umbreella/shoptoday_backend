from fastapi import status
from fastapi_jwt_auth import AuthJWT

url = '/api/transactions/'
token_admin = AuthJWT().create_access_token(subject='admin')
token_user = AuthJWT().create_access_token(subject='user')


async def test_When_GetForListTransactions_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForListTransactions_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForListTransactions_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForListTransactions_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListTransactions_Should_ErrorWith403(client):
    response = await client.get(url)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListTransactionsWithAuthUser_Should_NotFound(
        client, filling_users,
):
    response = await client.get(**{
        'url': url,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': 'Missing query_params "billing_account".',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForFilteredTransactionsWithAuthUser_Should_ErrorWith403(
        client, filling_transactions,
):
    response = await client.get(**{
        'url': f'{url}?billing_account=1',
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForListTransactionsWithAuthAdmin_Should_DataWith200(
        client, filling_transactions,
):
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
                'amount': 1_000,
                'bank_account_id': 1,
            },
            {
                'id': 2,
                'amount': 100,
                'bank_account_id': 2,
            },
        ],
        'previous_page': None,
        'next_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_GetForFilteredTransactionsWithAuthAdmin_Should_DataWith200(
        client, filling_transactions,
):
    response = await client.get(**{
        'url': f'{url}?billing_account=2',
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'items': [
            {
                'id': 2,
                'amount': 100,
                'bank_account_id': 2,
            },
        ],
        'previous_page': None,
        'next_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data
