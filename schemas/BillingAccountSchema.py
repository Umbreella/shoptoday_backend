from pydantic import BaseModel


class BankAccountSchema(BaseModel):
    id: int
    balance: float
    user_id: int

    class Config:
        orm_mode = True
