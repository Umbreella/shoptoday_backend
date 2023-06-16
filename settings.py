import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_ASYNC: str
    DATABASE_URL_SYNC: str

    class Config:
        env_file = os.getenv('ENV_FILE')


settings = Settings()
