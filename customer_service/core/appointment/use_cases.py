from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from common.config.settings import STR_FORMAT_HOURS
from common.custom_types.custom_types import CustomerID
from data_access.appointment.models import AppointmentDataType

from core.appointment.interfaces import CreateAppointmentUseCase
from core.google_calendar.models import EventData

if TYPE_CHECKING:
    from data_access.appointment.interfaces import BaseAppointmentWriterService
    from data_access.user.interfaces import BaseUserReaderService

    from core.appointment.models import AppointmentInputData
    from core.google_calendar.interfaces import BaseGoogleCalendarEventService


class CreateAppointmentUseCaseImpl(CreateAppointmentUseCase):
    __slots__ = (
        'appointment_writer_service',
        'google_calendar_event_service',
    )

    def __init__(
        self,
        user_reader_service: BaseUserReaderService,
        appointment_writer_service: BaseAppointmentWriterService,
        google_calendar_event_service: BaseGoogleCalendarEventService,
    ) -> None:
        self.user_reader_service = user_reader_service
        self.appointment_writer_service = appointment_writer_service
        self.google_calendar_event_service = google_calendar_event_service

    def __call__(
        self, appointment_input_data: AppointmentInputData, time_zone: str
    ) -> None:
        date, time = appointment_input_data.date_time.split('/')
        self.appointment_writer_service.create_appointment(
            appointment_data=AppointmentDataType(
                worker_id=appointment_input_data.worker_id,
                customer_id=CustomerID(
                    appointment_input_data.customer_credentials.user_id
                ),
                location_id=appointment_input_data.location_data.location_id,
                date=date,
                time=time,
            )
        )
        self._create_google_calendar_event(
            time_zone=time_zone,
            date=date,
            time=time,
            appointment_input_data=appointment_input_data,
        )

    def _create_google_calendar_event(
        self,
        time_zone: str,
        date: str,
        time: str,
        appointment_input_data: AppointmentInputData,
    ) -> None:
        if (
            appointment_input_data.customer_credentials.google_calendar_credentials
            is not None
            and (
                worker_name := self.user_reader_service.get_worker_name(
                    worker_id=appointment_input_data.worker_id
                )
            )
        ):
            start_time, end_time = self._prepare_appointment_hours(time=time)
            self.google_calendar_event_service.create_event(
                user_google_credentials=appointment_input_data.customer_credentials.google_calendar_credentials,
                event_data=EventData(
                    worker_name=worker_name,
                    address=appointment_input_data.location_data.address,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    time_zone=time_zone,
                ),
            )

    @staticmethod
    def _prepare_appointment_hours(time: str) -> tuple[datetime, datetime]:
        start_time = datetime.strptime(time, STR_FORMAT_HOURS)
        end_time = start_time + timedelta(hours=1)
        return start_time, end_time
