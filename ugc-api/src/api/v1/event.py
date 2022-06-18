import datetime
import json
from uuid import UUID

from aiokafka import AIOKafkaProducer
from core.config import settings
from fastapi import APIRouter
from models.event import Event

router = APIRouter()


@router.get("/", response_model=dict)
async def send_event(user_id: UUID, movie_id: UUID, time_frame: int, event_type: str) -> Event:
    data = Event(
        user_id=str(user_id),
        movie_id=str(movie_id),
        time_frame=time_frame,
        event_type=event_type,
        event_time=str(datetime.datetime.now()),
    )
    producer = AIOKafkaProducer(
        bootstrap_servers=[settings.KAFKA_HOST + ":" + settings.KAFKA_PORT], retry_backoff_ms=1000
    )
    await producer.start()
    await producer.send_and_wait(
        topic="views",
        value=json.dumps(dict(data)).encode("utf-8"),
        key=(data.user_id + "+" + data.movie_id).encode("utf-8"),
    )
    await producer.stop()

    return {"ok": "ok", **dict(data)}
