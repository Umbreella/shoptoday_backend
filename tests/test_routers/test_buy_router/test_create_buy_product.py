from copy import copy

from fastapi import status
from fastapi_jwt_auth import AuthJWT

url = '/api/buy/'
token_user = AuthJWT().create_access_token(subject='user')
data = {
    'product': 2,
    'billing_account': 2,
}


async def test_When_GetForBuyProduct_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForBuyProduct_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForBuyProduct_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForBuyProduct_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForBuyProductWithOutAuth_Should_ErrorWith403(client):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForBuyProductWithOutProducts_Should_ErrorWith400(
        client, filling_users,
):
    response = await client.post(**{
        'url': url,
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': {
            'product': 'Object does not exist.',
        }
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForBuyProductWithNoOwnerBilling_Should_ErrorWith400(
        client, filling_products, filling_billing_accounts,
):
    local_data = copy(data)
    local_data.update({
        'billing_account': 1,
    })

    response = await client.post(**{
        'url': url,
        'json': local_data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': {
            'billing_account': 'Object does not exist.',
        },
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForBuyProductWithOutFunds_Should_DataWith200(
        client, filling_products, filling_billing_accounts,
):
    local_data = copy(data)
    local_data.update({
        'product': 1,
    })

    response = await client.post(**{
        'url': url,
        'json': local_data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'status': 'Insufficient funds',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForBuyProductWithFunds_Should_DataWith200(
        client, filling_products, filling_billing_accounts,
):
    response = await client.post(**{
        'url': url,
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'status': 'Success',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data
