from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, select

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
