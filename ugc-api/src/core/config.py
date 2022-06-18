import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = "movies"
    KAFKA_HOST: str = "127.0.0.1"
    KAFKA_PORT: str = "9092"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SENTRY_DSN: str

    class Config:
        env_file = ".env"


settings = Settings()
