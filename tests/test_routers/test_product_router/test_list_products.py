from fastapi import status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import select

from models.ProductModel import ProductModel
from services.async_database import async_database

url = '/api/products/'
token_admin = AuthJWT().create_access_token(subject='admin')
token_user = AuthJWT().create_access_token(subject='user')
data = {
    'title': 'product',
    'description': 'product',
    'price': 10_000,
}


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


async def test_When_GetForListProducts_Should_ReturnDataWith200(
        client, filling_products,
):
    response = await client.get(url)

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'items': [
            {
                'id': 1,
                'title': 'product',
                'description': 'product',
                'price': 1000.0,
            },
        ],
        'next_page': None,
        'previous_page': None,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForListProductsWithNoAuth_Should_ErrorWith403(
        client, filling_users,
):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForListProductsWithUserAuth_Should_ErrorWith403(
        client, filling_users,
):
    response = await client.post(**{
        'url': url,
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForListProductsWithAdminAuth_Should_DataWith201(
        client, filling_users,
):
    response = await client.post(**{
        'url': url,
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    async with async_database.session() as db, db.begin():
        select_rows = await db.execute(select(ProductModel.id))
        select_result = select_rows.scalars().all()

    expected_status = status.HTTP_201_CREATED
    real_status = response.status_code

    expected_data = {
        **data,
        'id': 1,
    }
    real_data = response.json()

    expected_len_rows = 1
    real_len_rows = len(select_result)

    assert expected_status == real_status
    assert expected_data == real_data
    assert expected_len_rows == real_len_rows
