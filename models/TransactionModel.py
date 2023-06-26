from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.TransactionSchema import TransactionSchemaWebhook
from services.async_database import BASE


class TransactionModel(BASE):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    amount = Column(DECIMAL, nullable=False)

    bank_account_id = Column(ForeignKey('billing_accounts.id'), nullable=False)

    @classmethod
    async def get_all_query(cls, billing_account: int | None = None):
        query = select(cls)

        if billing_account:
            query = query.where(
                cls.bank_account_id == billing_account
            )

        return query.order_by(cls.id)

    @classmethod
    async def create(cls, data: TransactionSchemaWebhook, db: AsyncSession):
        insert_query = insert(cls).values({
            'id': data.transaction_id,
            'amount': data.amount,
            'bank_account_id': data.bill_id,
        }).on_conflict_do_nothing().returning(cls)

        insert_rows = await db.execute(insert_query)

        return insert_rows.scalars().first()
