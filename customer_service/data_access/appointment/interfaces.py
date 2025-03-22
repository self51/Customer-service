from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from common.custom_types.custom_types import WorkerID

    from data_access.appointment.models import AppointmentDataType


class BaseAppointmentReaderService(ABC):
    @abstractmethod
    def get_worker_appointment_times_for_date(
        self, worker_id: WorkerID, date: str
    ) -> list[str]:
        """Retrieves appointment times for specified worker ID and date."""


class BaseAppointmentWriterService(ABC):
    @abstractmethod
    def create_appointment(self, appointment_data: AppointmentDataType) -> None:
        """Creates appointment from provided appointment data."""
