from pydantic import BaseModel


class TransactionSchemaIn(BaseModel):
    signature: str
    transaction_id: int
    user_id: int
    bill_id: int
    amount: float
