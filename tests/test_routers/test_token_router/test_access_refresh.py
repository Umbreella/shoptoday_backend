from copy import copy

from fastapi import status
from fastapi_jwt_auth import AuthJWT

url = '/api/token/access/'
data = {
    'refresh': AuthJWT().create_refresh_token(subject='admin'),
}


async def test_When_GetForTokenAccess_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForTokenAccess_Should_ErrorWith405(client):
    response = await client.put(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForTokenAccess_Should_ErrorWith405(client):
    response = await client.patch(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForTokenAccess_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForTokenAccessWithRandomRefresh_Should_ErrorWith422(
        client,
):
    local_data = copy(data)
    local_data.update({
        'refresh': 'q' * 50,
    })

    response = await client.post(url, json=local_data)

    expected_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    real_status = response.status_code

    expected_data = {
        'detail': 'Not enough segments',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForTokenAccessWithAccessToken_Should_ErrorWith422(
        client,
):
    local_data = copy(data)
    local_data.update({
        'refresh': AuthJWT().create_access_token(subject='admin'),
    })

    response = await client.post(url, json=local_data)

    expected_status = status.HTTP_422_UNPROCESSABLE_ENTITY
    real_status = response.status_code

    expected_data = {
        'detail': 'Invalid token type.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForTokenAccessWithRefreshToken_Should_DataWith200(
        client,
):
    local_data = copy(data)

    response = await client.post(url, json=local_data)

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_keys = ('access',)
    real_keys = tuple(response.json().keys())

    assert expected_status == real_status
    assert expected_keys == real_keys
