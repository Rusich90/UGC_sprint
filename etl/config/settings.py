import yaml
from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    class Config:
        env_prefix = "KAFKA_"

    host: str
    group_id: str
    topics: str


class ClickhouseSettings(BaseSettings):
    class Config:
        env_prefix = "CLICKHOUSE_"

    host: str


class Settings(BaseSettings):
    analytics_db: ClickhouseSettings
    kafka: KafkaSettings
    backoff_ms: int
    backoff_max_ms: int
    max_row: int
    auto_offset_reset: str
    log_level: str


with open("config/config.yaml", "r") as file:
    data = yaml.safe_load(file)


settings = Settings(analytics_db=ClickhouseSettings(), kafka=KafkaSettings(), **data)
