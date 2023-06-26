from Crypto.Hash import SHA1
from fastapi import status
from sqlalchemy import select

from app.settings import settings
from models.TransactionModel import TransactionModel
from services.async_database import async_database

signature = SHA1.new()
signature.update(
    ':'.join((
        settings.PAYMENT_SECRET_KEY, '1', '1', '1', str(float(1000)),
    )).encode()
)

url = '/payment/webhook/'
data_with_valid_signature = {
    'signature': signature.hexdigest(),
    'transaction_id': 1,
    'user_id': 1,
    'bill_id': 1,
    'amount': 1000,
}
data_with_no_valid_signature = {
    'signature': 'q' * 50,
    'transaction_id': 1,
    'user_id': 1,
    'bill_id': 1,
    'amount': 100,
}


async def test_When_GetForPaymentWebhook_Should_ErrorWith405(client):
    response = await client.get(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PutForPaymentWebhook_Should_ErrorWith405(client):
    response = await client.put(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PatchForPaymentWebhook_Should_ErrorWith405(client):
    response = await client.patch(url, json={})

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_DeleteForPaymentWebhook_Should_ErrorWith405(client):
    response = await client.delete(url)

    expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
    real_status = response.status_code

    assert expected_status == real_status


async def test_When_PostForPaymentWebhookWithNoValid_Should_ErrorWith400(
        client,
):
    response = await client.post(url, json=data_with_no_valid_signature)

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': 'Not valid signature.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForPaymentWebhookWithUserNotFound_Should_ErrorWith400(
        client,
):
    response = await client.post(url, json=data_with_valid_signature)

    expected_status = status.HTTP_400_BAD_REQUEST
    real_status = response.status_code

    expected_data = {
        'detail': 'Not valid bill_id.',
    }
    real_data = response.json()

    assert expected_status == real_status
    assert expected_data == real_data


async def test_When_PostForPaymentWebhookWithBillNotFound_Should_NoneWith200(
        client, filling_users,
):
    response = await client.post(url, json=data_with_valid_signature)

    async with async_database.session() as db, db.begin():
        select_rows_transactions = await db.execute(
            select(TransactionModel)
        )
        select_result_transactions = select_rows_transactions.scalars().all()

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {}
    real_data = response.json()

    expected_count_transactions = 1
    real_count_transactions = len(select_result_transactions)

    assert expected_status == real_status
    assert expected_data == real_data
    assert expected_count_transactions == real_count_transactions


async def test_When_PostForPaymentWebhookWithBillingFound_Should_NoneWith200(
        client, filling_billing_accounts,
):
    response = await client.post(url, json=data_with_valid_signature)

    async with async_database.session() as db, db.begin():
        select_rows_transactions = await db.execute(
            select(TransactionModel)
        )
        select_result_transactions = select_rows_transactions.scalars().all()

    expected_status = status.HTTP_200_OK
    real_status = response.status_code

    expected_data = {}
    real_data = response.json()

    expected_count_transactions = 1
    real_count_transactions = len(select_result_transactions)

    assert expected_status == real_status
    assert expected_data == real_data
    assert expected_count_transactions == real_count_transactions
