from abc import ABC, abstractmethod

import backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import NetworkError


class AbstractAnalyticsDB(ABC):
    @abstractmethod
    def __init__(self, client):
        self.client = client

    @abstractmethod
    async def add(self, data: list[dict]) -> None:
        pass


class ClickhouseDB(AbstractAnalyticsDB):
    def __init__(self, client: Client):
        self.client = client

    @backoff.on_exception(backoff.expo, NetworkError)
    def add(self, data: list[dict]) -> None:
        self.client.execute(
            """
            INSERT INTO default.views (user_id, movie_id, time_frame, event_time, event_type) VALUES
            """,
            data,
        )
