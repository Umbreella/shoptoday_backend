from pydantic import BaseModel


class BothTokenSchema(BaseModel):
    access: str
    refresh: str
