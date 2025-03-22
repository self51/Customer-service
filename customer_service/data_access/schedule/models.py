from datetime import time

from pydantic import BaseModel, ConfigDict


class ScheduleHours(BaseModel):
    from_hour: time
    to_hour: time

    model_config = ConfigDict(from_attributes=True)
