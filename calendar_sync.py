from datetime import datetime, timedelta
import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import CALENDAR_ID, TIMEZONE


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def execute_with_retry(request, max_retries=6):
    """
    Voert een Google API-request uit.

    Bij een tijdelijke rate-limit fout (403/429)
    wacht het programma steeds langer en probeert
    het request opnieuw.
    """

    for attempt in range(max_retries):

        try:
            return request.execute()

        except HttpError as e:

            if e.resp.status in (403, 429):

                wait = 5 * (2 ** attempt)

                print(
                    f"Google API rate limit bereikt. "
                    f"Wachten {wait} seconden..."
                )

                time.sleep(wait)

            else:
                raise

    raise RuntimeError(
        "Google API blijft een rate limit geven. "
        "Synchronisatie gestopt."
    )


class GoogleCalendar:

    def __init__(self):

        creds = None
        token = "credentials/token.json"

        if os.path.exists(token):
            creds = Credentials.from_authorized_user_file(
                token,
                SCOPES
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:

                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials/credentials.json",
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open(token, "w") as f:
                f.write(creds.to_json())

        self.service = build(
            "calendar",
            "v3",
            credentials=creds
        )

    def build_index(self):

        events = []

        page_token = None

        while True:

            request = self.service.events().list(
                calendarId=CALENDAR_ID,
                pageToken=page_token,
                maxResults=2500,
                singleEvents=True
            )

            result = execute_with_retry(request)

            events.extend(result.get("items", []))

            page_token = result.get("nextPageToken")

            if not page_token:
                break

        index = {}

        for event in events:

            description = event.get("description", "")

            uid = None

            for line in description.splitlines():

                if line.startswith("UID:"):
                    uid = line.replace("UID:", "").strip()
                    break

            if uid:
                index[uid] = event

        return index

    def add_match(self, match):

        start = datetime.combine(
            match.date.date(),
            datetime.strptime(
                match.start_time,
                "%H:%M"
            ).time()
        )

        end = start + timedelta(hours=3)

        description = (
            f"{match.description}\n\n"
            f"UID:{match.uid}"
        )

        event = {
            "summary": match.title,

            "location": match.location,

            "description": description,

            "start": {
                "dateTime": start.isoformat(),
                "timeZone": TIMEZONE,
            },

            "end": {
                "dateTime": end.isoformat(),
                "timeZone": TIMEZONE,
            }
        }

        request = self.service.events().insert(
            calendarId=CALENDAR_ID,
            body=event
        )

        execute_with_retry(request)

        print("➕", match.title)

        time.sleep(1)

    def update_match(self, event, match):

        start = datetime.combine(
            match.date.date(),
            datetime.strptime(
                match.start_time,
                "%H:%M"
            ).time()
        )

        end = start + timedelta(hours=3)

        description = (
            f"{match.description}\n\n"
            f"UID:{match.uid}"
        )

        event["summary"] = match.title
        event["location"] = match.location
        event["description"] = description

        event["start"] = {
            "dateTime": start.isoformat(),
            "timeZone": TIMEZONE,
        }

        event["end"] = {
            "dateTime": end.isoformat(),
            "timeZone": TIMEZONE,
        }

        request = self.service.events().update(
            calendarId=CALENDAR_ID,
            eventId=event["id"],
            body=event
        )

        execute_with_retry(request)

        print("🔄", match.title)

        time.sleep(1)

    def delete_event(self, event):

        request = self.service.events().delete(
            calendarId=CALENDAR_ID,
            eventId=event["id"]
        )

        execute_with_retry(request)

        print("🗑️", event.get("summary", "Onbekende wedstrijd"))

        time.sleep(1)