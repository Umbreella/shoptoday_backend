from sqlalchemy import DECIMAL, Column, ForeignKey, Integer

from services.database import BASE


class BankAccountModel(BASE):
    __tablename__ = 'bank_accounts'

    id = Column(Integer, primary_key=True)
    balance = Column(DECIMAL, nullable=False)

    user_id = Column(ForeignKey('users.id'), nullable=False)
