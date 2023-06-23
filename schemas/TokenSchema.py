from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    access: str


class RefreshTokenSchema(BaseModel):
    refresh: str


class BothTokenSchema(RefreshTokenSchema, AccessTokenSchema):
    pass
