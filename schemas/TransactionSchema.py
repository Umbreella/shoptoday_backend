from pydantic import BaseModel


class TransactionSchemaWebhook(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: float


class TransactionSchemaOut(BaseModel):
    id: int
    amount: float
    bank_account_id: int

    class Config:
        orm_mode = True
