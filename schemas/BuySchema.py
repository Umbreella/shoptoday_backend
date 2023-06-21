from pydantic import BaseModel


class BuyProductSchema(BaseModel):
    product: int
    billing_account: int
