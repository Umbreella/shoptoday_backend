from pydantic import BaseModel


class ProductSchemaIn(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True


class ProductSchemaOut(BaseModel):
    id: int
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
