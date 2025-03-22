from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import TYPE_CHECKING

from common.config.settings import STR_FORMAT_HOURS, WEEKLY_SCHEDULE_DAYS
from django.utils import timezone

from core.schedule.interfaces import RetrieveWorkerScheduleUseCase
from core.schedule.models import DailySchedule, WeeklySchedule

if TYPE_CHECKING:
    from collections.abc import Generator

    from common.custom_types.custom_types import WorkerID
    from data_access.appointment.interfaces import BaseAppointmentReaderService
    from data_access.schedule.interfaces import BaseScheduleReaderService


class RetrieveWorkerScheduleUseCaseImpl(RetrieveWorkerScheduleUseCase):
    __slots__ = ('appointment_reader_service', 'schedule_reader_service')

    def __init__(
        self,
        appointment_reader_service: BaseAppointmentReaderService,
        schedule_reader_service: BaseScheduleReaderService,
    ) -> None:
        self.appointment_reader_service = appointment_reader_service
        self.schedule_reader_service = schedule_reader_service

    def __call__(
        self, worker_id: WorkerID, start_day: datetime = timezone.now().date()
    ) -> WeeklySchedule:
        return WeeklySchedule(
            previous_week_day=str(start_day - timedelta(WEEKLY_SCHEDULE_DAYS)),
            next_week_day=str(start_day + timedelta(WEEKLY_SCHEDULE_DAYS)),
            days=self._formate_daily_schedule(worker_id=worker_id, start_day=start_day),
        )

    def _formate_daily_schedule(
        self, worker_id: WorkerID, start_day: date
    ) -> list[DailySchedule]:
        return [
            DailySchedule(
                date=str(current_day),
                weekday=current_day.strftime('%A').upper(),
                hours=self._formate_hours_list(
                    worker_id=worker_id, current_day=current_day
                ),
            )
            for day_offset in range(WEEKLY_SCHEDULE_DAYS)
            if (current_day := start_day + timedelta(days=day_offset))
        ]

    def _formate_hours_list(self, worker_id: WorkerID, current_day: date) -> list[str]:
        weekday_number = current_day.weekday()
        current_day_booked_hours = (
            self.appointment_reader_service.get_worker_appointment_times_for_date(
                worker_id=worker_id, date=str(current_day)
            )
        )
        worker_schedules_hours = (
            self.schedule_reader_service.get_worker_schedules_hours_for_weekday(
                worker_id=worker_id, weekday_number=weekday_number
            )
        )
        return [
            hour
            for schedule_hours in worker_schedules_hours
            for hour in self._hour_list_generator(
                from_hour=schedule_hours.from_hour,
                to_hour=schedule_hours.to_hour,
                booked_hours=current_day_booked_hours,
            )
        ]

    @staticmethod
    def _hour_list_generator(
        from_hour: time, to_hour: time, booked_hours: list[str]
    ) -> Generator[str, None, None]:
        while from_hour <= to_hour:
            if (
                next_hour := from_hour.strftime(STR_FORMAT_HOURS)
            ) and next_hour not in booked_hours:
                yield next_hour
            from_hour = time(from_hour.hour + 1, from_hour.minute)
