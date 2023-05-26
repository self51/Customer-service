from datetime import datetime, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GoogleCalendarService:

    def __init__(self, user, worker, location, date, time):
        self.user = user
        self.worker = worker
        self.location = location.__str__()
        self.date = date
        self.start_time = datetime.strptime(time, "%H:%M")
        self.end_time = self.start_time + timedelta(hours=1)
        self.time_zone = "+0300"  # ukraine Kyiv by default

    def load_credentials(self):
        """ Loads credentials from the DB."""
        credentials_dict = self.user.google_calendar_credentials
        credentials = Credentials(
            credentials_dict['token'],
            credentials_dict['refresh_token'],
            credentials_dict['token_uri'],
            credentials_dict['client_id'],
            credentials_dict['client_secret'],
            credentials_dict['scopes'],
        )
        return credentials

    def create_service(self):
        """Use the Google API Discovery Service to build client libraries, IDE plugins,
        and other tools that interact with Google APIs.
        The Discovery API provides a list of Google APIs and a machine-readable "Discovery Document" for each API"""
        service = build("calendar", "v3", credentials=self.load_credentials())
        return service

    def create_event(self):
        """Creates an event in the user's Google calendar"""

        # dateTime required format is '{year}-{month}-{day}T{H:M:S}{time_zone}'
        event = {
            'summary': 'Customer service appointment - {}'.format(self.worker),
            'location': self.location,
            'description': 'This is appointment to your providing service',
            'start': {
                'dateTime': f'{self.date}T{self.start_time.strftime("%H:%M:%S")}{self.time_zone}',
            },
            'end': {
                'dateTime': f'{self.date}T{self.end_time.strftime("%H:%M:%S")}{self.time_zone}',
            },
        }

        self.create_service().events().insert(calendarId='primary', body=event).execute()
