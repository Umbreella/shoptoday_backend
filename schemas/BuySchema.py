from pydantic import BaseModel


class BuyProductSchema(BaseModel):
    product: int
    billing_account: int


class BuyStatus(BaseModel):
    status: str
