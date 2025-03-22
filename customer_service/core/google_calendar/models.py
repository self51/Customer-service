from datetime import datetime

from pydantic import BaseModel


class EventData(BaseModel):
    worker_name: str
    address: str
    date: str
    start_time: datetime
    end_time: datetime
    time_zone: str
