import json
import logging.config
import time

from clickhouse_driver import Client
from config.logger_config import LOGGING_CONFIG
from config.settings import settings
from confluent_kafka import Consumer

from db.database import AbstractAnalyticsDB, ClickhouseDB

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("etl")


def etl_process(analytics_db: AbstractAnalyticsDB, consumer: Consumer) -> None:
    consumer.subscribe(settings.kafka.topics.split(","))
    running = True

    while running:
        try:
            msg_list = consumer.consume(num_messages=settings.max_row, timeout=1)

            if not msg_list:
                logger.debug("no message...")
                time.sleep(10)
                continue

            else:
                new_data = [json.loads(msg.value()) for msg in msg_list]
                analytics_db.add(new_data)
                logger.info(f"Sent in clickhouse {len(msg_list)} rows")
                consumer.commit(msg_list[-1])

        except json.decoder.JSONDecodeError:
            logger.error("Not JSON in message")

        except KeyboardInterrupt:
            break

    consumer.close()


if __name__ == "__main__":
    clickhouse = Client(host=settings.analytics_db.host)
    analytics_db = ClickhouseDB(clickhouse)
    consumer = Consumer(
        {
            "bootstrap.servers": settings.kafka.host,
            "group.id": settings.kafka.group_id,
            "reconnect.backoff.ms": settings.backoff_ms,
            "reconnect.backoff.max.ms": settings.backoff_max_ms,
            "auto.offset.reset": settings.auto_offset_reset,
            "enable.auto.commit": False,
        }
    )
    logger.info("ETL process started ")
    etl_process(analytics_db, consumer)
