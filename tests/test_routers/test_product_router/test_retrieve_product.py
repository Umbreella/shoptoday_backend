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


async def test_When_PatchForSingleProduct_Should_ErrorWith405(client):
    response = await client.patch(f'{url}1/', json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForSingleRandomProduct_Should_NotFound(client):
    response = await client.get(f'{url}1/')

    expected_status = status.HTTP_404_NOT_FOUND
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_GetForSingleProduct_Should_ReeturnDataWith200(
        client, filling_products,
):
    response = await client.get(f'{url}1/')

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {
        'id': 1,
        'title': 'product',
        'description': 'product',
        'price': 1_000,
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PutForSingleProductWithOutAuth_Should_ErrorWith403(
        client,
):
    response = await client.put(f'{url}1/', json=data)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSingleProductWithUserAuth_Should_ErrorWith403(
        client, filling_users,
):
    response = await client.put(**{
        'url': f'{url}1/',
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSingleProductWithAdminAuth_Should_NotFound(
        client, filling_users,
):
    response = await client.put(**{
        'url': f'{url}1/',
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status = status.HTTP_404_NOT_FOUND
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSingleProductWithAdminAuth_Should_DataWith200(
        client, filling_users, filling_products,
):
    response = await client.put(**{
        'url': f'{url}1/',
        'json': data,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    async with async_database.session() as db, db.begin():
        select_rows = await db.execute(
            select(ProductModel).where(ProductModel.id == 1)
        )
        select_result = select_rows.scalars().first()

        update_product = {
            'id': select_result.id,
            'title': select_result.title,
            'description': select_result.description,
            'price': select_result.price,
        }

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = update_product
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_DeleteForSingleProductWithOutAuth_Should_ErrorWith403(
        client,
):
    response = await client.delete(f'{url}1/')

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSingleProductWithUserAuth_Should_ErrorWith403(
        client, filling_users,
):
    response = await client.delete(**{
        'url': f'{url}1/',
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSingleProductWithAdminAuth_Should_NotFound(
        client, filling_users,
):
    response = await client.delete(**{
        'url': f'{url}1/',
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status = status.HTTP_404_NOT_FOUND
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSingleProductWithAdminAuth_Should_DataWith204(
        client, filling_users, filling_products,
):
    response = await client.delete(**{
        'url': f'{url}1/',
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    async with async_database.session() as db, db.begin():
        select_rows = await db.execute(
            select(ProductModel).where(ProductModel.id == 1)
        )
        select_result = select_rows.scalars().first()

    expected_status = status.HTTP_204_NO_CONTENT
    real_status = response.status_code

    expected_len_rows = None
    real_len_rows = select_result

    assert expected_status == real_status
    assert expected_len_rows == real_len_rows
