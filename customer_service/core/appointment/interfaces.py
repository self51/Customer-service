from typing import Protocol

from core.appointment.models import AppointmentInputData


class CreateAppointmentUseCase(Protocol):
    def __call__(
        self, appointment_input_data: AppointmentInputData, time_zone: str
    ) -> None:
        """Creates appointment for user from input data.

        Args:
            appointment_input_data: The appointment input data to create appointment for.
            time_zone: The time zone for the appointment.

        """
