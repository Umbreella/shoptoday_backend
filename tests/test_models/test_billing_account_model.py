from sqlalchemy import select

from models.BillingAccountModel import BillingAccountModel
from schemas.BillingAccountSchema import BillingAccountSchema
from services.async_database import async_database

tested_class = BillingAccountModel


async def test_When_CallCheckOwnerWithOutBillAccount_Should_ReturnFalse(
        filling_users,
):
    async with async_database.session() as db, db.begin():
        is_owner = await tested_class.check_owner(1, 1, db)

    expected_is_owner = False
    real_is_owner = is_owner

    assert expected_is_owner == real_is_owner


async def test_When_CallCheckOwnerWithOutOwner_Should_ReturnFalse(
        filling_billing_accounts,
):
    async with async_database.session() as db, db.begin():
        is_owner = await tested_class.check_owner(1, 2, db)

    expected_is_owner = False
    real_is_owner = is_owner

    assert expected_is_owner == real_is_owner


async def test_When_CallCheckOwnerWithOwner_Should_ReturnTrue(
        filling_billing_accounts,
):
    async with async_database.session() as db, db.begin():
        is_owner = await tested_class.check_owner(1, 1, db)

    expected_is_owner = True
    real_is_owner = is_owner

    assert expected_is_owner == real_is_owner


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
            tested_class.user_id == 1
        ).order_by(
            tested_class.id
        ))
    real_query = str(await tested_class.get_all_query(1))

    assert expected_query == real_query


async def test_When_CallGetOrCreateWithUserNotFound_Should_ReturnNone():
    has_exception = False
    try:
        async with async_database.session() as db, db.begin():
            await tested_class.get_or_create(1, 1, db)
    except Exception:
        has_exception = True

    expected_has_exception = True
    real_has_exception = has_exception

    assert expected_has_exception == real_has_exception


async def test_When_CallGetOrCreateWithUser_Should_ReturnCreateBillAccount(
        filling_users,
):
    async with async_database.session() as db, db.begin():
        billing_account_orm = await tested_class.get_or_create(1, 1, db)
        billing_account = BillingAccountSchema.from_orm(billing_account_orm)

    expected_billing_accounts = {
        'id': 1,
        'balance': 0,
        'user_id': 1,
    }
    real_billing_account = billing_account

    assert expected_billing_accounts == real_billing_account


async def test_When_CallGetOrCreateWithBillingAccount_Should_ReturnExisted(
        filling_billing_accounts,
):
    async with async_database.session() as db, db.begin():
        billing_account_orm = await tested_class.get_or_create(1, 1, db)
        billing_account = BillingAccountSchema.from_orm(billing_account_orm)

    expected_billing_accounts = {
        'id': 1,
        'balance': 1_000,
        'user_id': 1,
    }
    real_billing_account = billing_account

    assert expected_billing_accounts == real_billing_account


async def test_When_CallUpdateBalanceManySub_Should_DontChangeBalance(
        filling_billing_accounts,
):
    async with async_database.session() as db, db.begin():
        status = await tested_class.update_balance(1, -10_000, db)

    async with async_database.session() as db, db.begin():
        select_rows = await db.execute(
            select(tested_class).where(tested_class.id == 1)
        )
        balance = select_rows.scalars().first().balance

    expected_status = 'Insufficient funds'
    real_status = status

    expected_balance = 1_000
    real_balance = balance

    assert expected_status == real_status
    assert expected_balance == real_balance


async def test_When_CallUpdateBalanceSub_Should_ChangeBalance(
        filling_billing_accounts,
):
    async with async_database.session() as db, db.begin():
        status = await tested_class.update_balance(1, -1_000, db)

        select_rows = await db.execute(
            select(tested_class).where(tested_class.id == 1)
        )
        select_result = select_rows.scalars().first()

        balance = select_result.balance

    expected_status = 'Success'
    real_status = status

    expected_balance = 0
    real_balance = balance

    assert expected_status == real_status
    assert expected_balance == real_balance
