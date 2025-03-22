from __future__ import annotations

from typing import TYPE_CHECKING, Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build

from integrations.google.interfaces import GoogleServiceFactory

if TYPE_CHECKING:
    from integrations.google.enums import GoogleServiceNameEnum


class GoogleServiceFactoryImpl(GoogleServiceFactory):
    def __call__(
        self,
        user_google_credentials: dict[str, Any],
        google_service_name: GoogleServiceNameEnum,
        service_version: str = 'v3',
    ) -> Resource:
        return build(
            serviceName=google_service_name,
            version=service_version,
            credentials=self._load_credentials_for_user(
                user_credentials=user_google_credentials
            ),
        )

    @staticmethod
    def _load_credentials_for_user(user_credentials: dict[str, Any]) -> Credentials:
        return Credentials(
            token=user_credentials.get('token'),
            refresh_token=user_credentials.get('refresh_token'),
            token_uri=user_credentials.get('token_uri'),
            client_id=user_credentials.get('client_id'),
            client_secret=user_credentials.get('client_secret'),
            scopes=user_credentials.get('scopes'),
        )
