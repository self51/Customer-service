from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

from django.utils import timezone

if TYPE_CHECKING:
    from datetime import datetime

    from common.custom_types.custom_types import WorkerID

    from core.schedule.models import WeeklySchedule


class RetrieveWorkerScheduleUseCase(Protocol):
    def __call__(
        self, worker_id: WorkerID, start_day: datetime = timezone.now()
    ) -> WeeklySchedule:
        """Retrieves a weekly schedule for a given start day and worker ID.

        Args:
            worker_id: The worker ID.
            start_day: The start day of week to retrieve weekly schedule for.

        Returns:
            The weekly schedule for the given start day and worker ID.

        """
