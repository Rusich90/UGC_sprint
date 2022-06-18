from pydantic import BaseModel


class Event(BaseModel):
    user_id: str
    movie_id: str
    time_frame: int
    event_type: str
    event_time: str
