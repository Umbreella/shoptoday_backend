from sqlalchemy import select

from models.TransactionModel import TransactionModel
from schemas.TransactionSchema import (TransactionSchemaOut,
                                       TransactionSchemaWebhook)
from services.async_database import async_database

tested_class = TransactionModel


async def test_When_CallGetAllQueryWithOutArgs_Should_SelectWithOrderBy():
    expected_query = str(
        select(
            tested_class
        ).order_by(
            tested_class.id
        ))
    real_query = str(await tested_class.get_all_query())

    assert expected_query == real_query


async def test_When_CallGetAllQueryWithArgs_Should_SelectWithWhereAndOrderBy():
    expected_query = str(
        select(
            tested_class
        ).where(
            tested_class.bank_account_id == 1
        ).order_by(
            tested_class.id
        ))
    real_query = str(await tested_class.get_all_query(1))

    assert expected_query == real_query


async def test_When_CallCreate_Should_CreateNewRowInTable(
        filling_billing_accounts,
):
    data = TransactionSchemaWebhook(**{
        'signature': '',
        'transaction_id': 1,
        'user_id': 1,
        'bill_id': 1,
        'amount': 1_000,
    })

    async with async_database.session() as db, db.begin():
        transaction_orm = await tested_class.create(data, db)
        transaction = TransactionSchemaOut.from_orm(transaction_orm)

    expected_amount = 1_000
    real_amount = transaction.amount

    expected_billing_account_id = 1
    real_billing_account_id = transaction.bank_account_id

    assert expected_amount == real_amount
    assert expected_billing_account_id == real_billing_account_id


async def test_When_CallCreateWithNotFoungBilling_Should_CreateNewRowInTable():
    data = TransactionSchemaWebhook(**{
        'signature': '',
        'transaction_id': 1,
        'user_id': 1,
        'bill_id': 1,
        'amount': 1_000,
    })

    has_exception = False

    async with async_database.session() as db, db.begin():
        try:
            await tested_class.create(data, db)
        except Exception:
            has_exception = True

    expected_has_exception = 1
    real_has_exception = has_exception

    assert expected_has_exception == real_has_exception
