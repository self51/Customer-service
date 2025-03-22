from __future__ import annotations

from typing import TYPE_CHECKING

from common.config.settings import STR_FORMAT_HOURS

from data_access.appointment.interfaces import (
    BaseAppointmentReaderService,
    BaseAppointmentWriterService,
)

if TYPE_CHECKING:
    from appointment.models import Appointment
    from common.custom_types.custom_types import WorkerID

    from data_access.appointment.models import AppointmentDataType


class AppointmentReaderService(BaseAppointmentReaderService):
    __slots__ = ('appointment_model',)

    def __init__(self, appointment_model: type[Appointment]) -> None:
        self.appointment_model = appointment_model

    def get_worker_appointment_times_for_date(
        self, worker_id: WorkerID, date: str
    ) -> list[str]:
        return [
            appointment.time.strftime(STR_FORMAT_HOURS)
            for appointment in self.appointment_model.objects.filter(
                worker=worker_id, date=date
            ).only('time')
        ]


class AppointmentWriterService(BaseAppointmentWriterService):
    __slots__ = ('appointment_model',)

    def __init__(self, appointment_model: type[Appointment]) -> None:
        self.appointment_model = appointment_model

    def create_appointment(self, appointment_data: AppointmentDataType) -> None:
        self.appointment_model.objects.create(**appointment_data.model_dump())
