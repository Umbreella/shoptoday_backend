from sqlalchemy import DECIMAL, Column, ForeignKey, Integer

from services.database import BASE


class TransactionModel(BASE):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    balance = Column(DECIMAL, nullable=False)

    bank_account_id = Column(ForeignKey('bank_accounts.id'), nullable=False)
