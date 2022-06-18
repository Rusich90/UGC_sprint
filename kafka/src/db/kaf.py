from core.config import settings

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=[settings.KAFKA_HOST + ":" + settings.KAFKA_PORT], retries=5)
