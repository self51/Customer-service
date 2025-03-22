from __future__ import annotations

from typing import TYPE_CHECKING, Any

from integrations.google.enums import GoogleServiceNameEnum

from core.google_calendar.interfaces import BaseGoogleCalendarEventService

if TYPE_CHECKING:
    from integrations.google.interfaces import GoogleServiceFactory

    from core.google_calendar.models import EventData


class GoogleCalendarEventService(BaseGoogleCalendarEventService):
    __slots__ = ('google_service_factory',)

    def __init__(self, google_service_factory: GoogleServiceFactory) -> None:
        self.google_service_factory = google_service_factory

    def create_event(
        self, user_google_credentials: dict[str, Any], event_data: EventData
    ) -> None:
        event = {
            'summary': f'Customer service appointment - {event_data.worker_name}',
            'location': event_data.address,
            'description': 'This is appointment to your providing service',
            'start': {
                'dateTime': f'{event_data.date}T{event_data.start_time.strftime("%H:%M:%S")}{event_data.time_zone}',
            },
            'end': {
                'dateTime': f'{event_data.date}T{event_data.end_time.strftime("%H:%M:%S")}{event_data.time_zone}',
            },
        }
        self.google_service_factory(
            user_google_credentials=user_google_credentials,
            google_service_name=GoogleServiceNameEnum.CALENDAR,
        ).events().insert(calendarId='primary', body=event).execute()
