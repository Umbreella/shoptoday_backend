from pydantic import BaseModel


class BillingAccountSchema(BaseModel):
    id: int
    balance: float
    user_id: int

    class Config:
        orm_mode = True
