from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.custom_types.custom_types import WorkerID

    from data_access.schedule.models import ScheduleHours


class BaseScheduleReaderService(ABC):
    @abstractmethod
    def get_worker_schedules_hours_for_weekday(
        self, worker_id: WorkerID, weekday_number: int
    ) -> list[ScheduleHours]:
        """Retrieves worker schedule hours data for a given worker ID and weekday number."""
