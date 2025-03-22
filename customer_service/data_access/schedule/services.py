from __future__ import annotations

from typing import TYPE_CHECKING

from data_access.schedule.interfaces import BaseScheduleReaderService
from data_access.schedule.models import ScheduleHours

if TYPE_CHECKING:
    from common.custom_types.custom_types import WorkerID
    from worker.models import Schedule


class ScheduleReaderService(BaseScheduleReaderService):
    __slots__ = ('schedule_model',)

    def __init__(self, schedule_model: type[Schedule]) -> None:
        self.schedule_model = schedule_model

    def get_worker_schedules_hours_for_weekday(
        self, worker_id: WorkerID, weekday_number: int
    ) -> list[ScheduleHours]:
        return [
            ScheduleHours.model_validate(schedule)
            for schedule in self.schedule_model.objects.filter(
                worker=worker_id, weekday=weekday_number
            ).only('from_hour', 'to_hour')
        ]
