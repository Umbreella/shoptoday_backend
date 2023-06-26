import os

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_HOST: str
    DATABASE_URL_PORT: str
    DATABASE_URL_USER: str
    DATABASE_URL_PASSWORD: str
    DATABASE_URL_DB: str
    PAYMENT_SECRET_KEY: str
    authjwt_algorithm: str
    authjwt_secret_key: str
    authjwt_access_token_expires: int
    authjwt_refresh_token_expires: int

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
