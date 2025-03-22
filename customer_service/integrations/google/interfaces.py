from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from googleapiclient.discovery import Resource

    from integrations.google.enums import GoogleServiceNameEnum


class GoogleServiceFactory(Protocol):
    __slots__ = ('user_reader_service',)

    def __call__(
        self,
        user_google_credentials: dict[str, Any],
        google_service_name: GoogleServiceNameEnum,
        service_version: str = 'v3',
    ) -> Resource:
        """Retrieves constructed a resource for interacting with Google API.

        Args:
            user_google_credentials: The dictionary with user google calendar credentials data.
            google_service_name: The name of the Google API service to construct.
            service_version: The version of the API service to construct.

        Returns: The constructed resource.

        """
