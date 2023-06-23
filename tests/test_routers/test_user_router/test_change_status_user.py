from fastapi import status
from fastapi_jwt_auth import AuthJWT

url = '/api/users/2/'
url_not_found = '/api/users/10/'
json_data_activate = {
    'is_active': True,
}
json_data_deactivate = {
    'is_active': False,
}
token_admin = AuthJWT().create_access_token(subject='admin')
token_user = AuthJWT().create_access_token(subject='user')


async def test_When_GetForSingleUser_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForSingleUser_Should_ErrorWith405(client):
    response = await client.post(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSingleUser_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSingleUser_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSingleUserWithNotValidBody_Should_ErrorWith422(
        client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSingleUserWithOutAuthUser_Should_ErrorWith403(
        client):
    response = await client.patch(url, json=json_data_activate)

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSingleUserWithRandomAuth_Should_ErrorWith403(
        client, filling_users,
):
    response = await client.patch(**{
        'url': url,
        'json': json_data_activate,
        'headers': {
            'Authorization': f'Bearer {token_user}',
        },
    })

    expected_status = status.HTTP_403_FORBIDDEN
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForNotFoundUserWithAdminAuth_Should_NotFound(
        client, filling_users,
):
    response = await client.patch(**{
        'url': url_not_found,
        'json': json_data_activate,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status = status.HTTP_404_NOT_FOUND
    real_status = response.status_code

    expected_data = {
        'detail': 'Not found.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PatchForSingleUserWithAdminAuth_Should_ChangeIsActive(
        client, filling_users,
):
    response_activate = await client.patch(**{
        'url': url,
        'json': json_data_activate,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    response_deactivate = await client.patch(**{
        'url': url,
        'json': json_data_deactivate,
        'headers': {
            'Authorization': f'Bearer {token_admin}',
        },
    })

    expected_status_activate = status.HTTP_200_OK
    real_status_activate = response_activate.status_code

    expected_data_activate = True
    real_data_activate = response_activate.json().get('is_active')

    expected_status_deactivate = status.HTTP_200_OK
    real_status_deactivate = response_deactivate.status_code

    expected_data_deactivate = False
    real_data_deactivate = response_deactivate.json().get('is_active')

    assert expected_status_activate == real_status_activate
    assert expected_data_activate == real_data_activate

    assert expected_status_deactivate == real_status_deactivate
    assert expected_data_deactivate == real_data_deactivate
