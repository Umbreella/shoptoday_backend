import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_ASYNC: str
    DATABASE_URL_SYNC: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    PAYMENT_SECRET_KEY: str
    authjwt_secret_key: str

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
