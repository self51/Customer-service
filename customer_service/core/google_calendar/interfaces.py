from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from core.google_calendar.models import EventData


class BaseGoogleCalendarEventService(ABC):
    @abstractmethod
    def create_event(
        self, user_google_credentials: dict[str, Any], event_data: EventData
    ) -> None:
        """Creates event in user Google Calendar based on event data.

        Args:
            user_google_credentials: The dictionary with user google calendar credentials data.
            event_data: The event data.

        """
