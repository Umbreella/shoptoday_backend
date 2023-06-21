from pydantic import BaseModel


class UserSchemaIn(BaseModel):
    username: str
    password: str


class UserSchemaOut(BaseModel):
    id: int
    username: str
    password: str
    is_superuser: bool
    is_active: bool

    class Config:
        orm_mode = True


class UserSchemaStatus(BaseModel):
    is_active: bool
