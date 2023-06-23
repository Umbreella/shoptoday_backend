from fastapi import status

url = '/api/sign_up/'
data = {
    'username': 'test',
    'password': 'test',
}


async def test_When_GetForSignUp_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForSignUp_Should_ErrorWith405(client):
    response = await client.put(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForSignUp_Should_ErrorWith405(client):
    response = await client.patch(url, json=data)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForSignUp_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForSignUpWithDuplicateUsername_Should_ErrorWith400(
        client, filling_users,
):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': 'This username is used.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForSignUp_Should_DataWith201(client):
    response = await client.post(url, json=data)

    expected_status = status.HTTP_201_CREATED
    real_status = response.status_code

    expected_activate_url = None
    real_activate_url = response.json().get('activate_url')

    assert expected_status == real_status
    assert expected_activate_url != real_activate_url
