import datetime
import json
from uuid import UUID

from fastapi import APIRouter

from db.kaf import producer

router = APIRouter()


@router.get("/", response_model=dict)
async def send_event(user_id: UUID, film_id: UUID, time_frame: int, event_type: str) -> dict:
    data = {
        "user_id": str(user_id),
        "film_id": str(film_id),
        "time_frame": time_frame,
        "event_type": event_type,
        "timestamp": str(datetime.datetime.now()),
    }
    producer.send(
        topic="views",
        value=json.dumps(data).encode("utf-8"),
        key=(str(user_id) + "+" + str(film_id)).encode("utf-8"),
    )

    return {
        "ok": "ok",
        "user_id": user_id,
        "film_id": film_id,
        "time_frame": time_frame,
        "event_type": event_type,
        "timestamp": str(datetime.datetime.now()),
    }
