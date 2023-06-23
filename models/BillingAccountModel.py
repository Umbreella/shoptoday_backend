from sqlalchemy import (DECIMAL, CheckConstraint, Column, ForeignKey, Integer,
                        and_, select, update)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.async_database import BASE


class BillingAccountModel(BASE):
    __tablename__ = 'billing_accounts'

    __table_args__ = (
        CheckConstraint('balance >= 0', 'only_positive_balance'),
    )

    id = Column(Integer, primary_key=True)
    balance = Column(DECIMAL, nullable=False, default=0)

    user_id = Column(ForeignKey('users.id'), nullable=False)

    @classmethod
    async def check_owner(cls, user_id: int, billing_account_id: int,
                          db: AsyncSession) -> bool:
        query = select(cls).where(and_(
            cls.id == billing_account_id,
            cls.user_id == user_id,
        ))

        rows = await db.execute(query)
        result = rows.scalars().first()

        return bool(result)

    @classmethod
    async def get_all_query(cls, user_id: int | None = None):
        query = select(cls)

        if user_id:
            query = query.where(
                cls.user_id == user_id
            )

        return query.order_by(cls.id)

    @classmethod
    async def get_or_create(cls, user_id: int, billing_account_id: int,
                            db: AsyncSession):
        select_query = select(cls).where(and_(
            cls.id == billing_account_id,
            cls.user_id == user_id,
        ))

        select_rows = await db.execute(select_query)
        select_result = select_rows.scalars().first()

        if select_result:
            return select_result

        insert_query = insert(cls).values({
            'id': billing_account_id,
            'user_id': user_id,
        }).on_conflict_do_nothing().returning(cls)

        insert_rows = await db.execute(insert_query)
        insert_result = insert_rows.scalars().first()

        return insert_result

    @classmethod
    async def update_balance(cls, billing_account_id: int,
                             change_balance: float, db: AsyncSession):
        update_query = update(cls).where(
            cls.id == billing_account_id
        ).values({
            'balance': cls.balance + change_balance,
        }).returning(cls.id)

        try:
            await db.execute(update_query)
        except IntegrityError:
            return 'Insufficient funds'

        return 'Success'
