from __future__ import annotations

from typing import TYPE_CHECKING

from appointment.models import Appointment
from authentication.models import User
from core.appointment.use_cases import CreateAppointmentUseCaseImpl
from core.google_calendar.services import GoogleCalendarEventService
from core.schedule.use_cases import RetrieveWorkerScheduleUseCaseImpl
from data_access.appointment.services import (
    AppointmentReaderService,
    AppointmentWriterService,
)
from data_access.schedule.services import ScheduleReaderService
from data_access.user.services import UserReaderService
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Factory
from integrations.google.services import GoogleServiceFactoryImpl
from worker.models import Schedule

if TYPE_CHECKING:
    from core.appointment.interfaces import CreateAppointmentUseCase
    from core.google_calendar.interfaces import BaseGoogleCalendarEventService
    from core.schedule.interfaces import RetrieveWorkerScheduleUseCase
    from data_access.appointment.interfaces import (
        BaseAppointmentReaderService,
        BaseAppointmentWriterService,
    )
    from data_access.schedule.interfaces import BaseScheduleReaderService
    from data_access.user.interfaces import BaseUserReaderService
    from integrations.google.interfaces import GoogleServiceFactory

WIRING_MODULES: tuple[str, ...] = (
    'appointment.views',
    'authentication.views',
)


class DependencyContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=WIRING_MODULES)
    config = Configuration()

    # External integrations
    google_service_factory: Factory[GoogleServiceFactory] = Factory(
        GoogleServiceFactoryImpl
    )

    # Repositories
    appointment_reader_service: Factory[BaseAppointmentReaderService] = Factory(
        AppointmentReaderService, appointment_model=Appointment
    )
    appointment_writer_service: Factory[BaseAppointmentWriterService] = Factory(
        AppointmentWriterService, appointment_model=Appointment
    )

    schedule_reader_service: Factory[BaseScheduleReaderService] = Factory(
        ScheduleReaderService, schedule_model=Schedule
    )

    user_reader_service: Factory[BaseUserReaderService] = Factory(
        UserReaderService, user_model=User
    )

    # Services
    google_calendar_event_service: Factory[BaseGoogleCalendarEventService] = Factory(
        GoogleCalendarEventService,
        google_service_factory=google_service_factory,
    )

    # Use Cases
    # Appointment
    create_appointment_u_c: Factory[CreateAppointmentUseCase] = Factory(
        CreateAppointmentUseCaseImpl,
        user_reader_service=user_reader_service,
        appointment_writer_service=appointment_writer_service,
        google_calendar_event_service=google_calendar_event_service,
    )

    # Schedule
    retrieve_worker_schedule_u_c: Factory[RetrieveWorkerScheduleUseCase] = Factory(
        RetrieveWorkerScheduleUseCaseImpl,
        appointment_reader_service=appointment_reader_service,
        schedule_reader_service=schedule_reader_service,
    )
