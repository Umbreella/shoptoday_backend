from typing import List

import pytest
from sqlalchemy import insert

from models.BillingAccountModel import BillingAccountModel
from models.ProductModel import ProductModel
from models.TransactionModel import TransactionModel
from models.UserModel import UserModel
from services.async_database import async_database
from services.security import security


@pytest.fixture
async def filling_products() -> None:
    async with async_database.session() as db, db.begin():
        await db.execute(
            insert(
                ProductModel
            ).values([
                {
                    'id': 1,
                    'title': 'product',
                    'description': 'product',
                    'price': 1_000,
                },
                {
                    'id': 2,
                    'title': 'product',
                    'description': 'product',
                    'price': 100,
                },
            ])
        )


@pytest.fixture
async def filling_users() -> None:
    async with async_database.session() as db, db.begin():
        await db.execute(
            insert(
                UserModel
            ).values([
                {
                    'id': 1,
                    'username': 'admin',
                    'password': 'admin',
                    'is_superuser': True,
                    'is_active': True,
                },
                {
                    'id': 2,
                    'username': 'user',
                    'password': 'user',
                    'is_superuser': False,
                    'is_active': False,
                },
            ])
        )


@pytest.fixture
async def filling_users_with_passwords() -> List[str]:
    async with async_database.session() as db, db.begin():
        insert_rows = await db.execute(
            insert(
                UserModel
            ).values([
                {
                    'id': 1,
                    'username': 'admin',
                    'password': security.get_password_hash('admin'),
                    'is_superuser': True,
                    'is_active': True,
                },
                {
                    'id': 2,
                    'username': 'user',
                    'password': security.get_password_hash('user'),
                    'is_superuser': False,
                    'is_active': False,
                },
            ]).returning(UserModel.password)
        )

        return insert_rows.scalars().all()


@pytest.fixture
async def filling_billing_accounts(filling_users) -> None:
    async with async_database.session() as db, db.begin():
        await db.execute(
            insert(
                BillingAccountModel
            ).values([
                {
                    'id': 1,
                    'balance': 1_000,
                    'user_id': 1,
                },
                {
                    'id': 2,
                    'balance': 100,
                    'user_id': 2,
                },
            ])
        )


@pytest.fixture
async def filling_transactions(filling_billing_accounts) -> None:
    async with async_database.session() as db, db.begin():
        await db.execute(
            insert(
                TransactionModel
            ).values([
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
            ])
        )
