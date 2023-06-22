import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_HOST: str
    DATABASE_URL_PORT: str
    DATABASE_URL_USER: str
    DATABASE_URL_PASSWORD: str
    DATABASE_URL_DB: str
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
