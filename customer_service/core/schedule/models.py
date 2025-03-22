from pydantic import BaseModel


class DailySchedule(BaseModel):
    date: str
    weekday: str
    hours: list[str]


class WeeklySchedule(BaseModel):
    previous_week_day: str
    next_week_day: str
    days: list[DailySchedule]
