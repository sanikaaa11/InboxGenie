# tools/calendar_tool.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import pytz

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("calendar", "v3", credentials=creds)


def create_event(summary, start_iso, end_iso, description="", timezone_name="Asia/Kolkata"):
    """
    Creates a calendar event using ISO datetime strings.
    Always uses a valid IANA timezone (Asia/Kolkata).
    """

    service = get_calendar_service()

    # Ensure valid timezone
    tz = pytz.timezone(timezone_name)

    # Convert ISO strings to timezone-aware datetimes
    start_dt = tz.localize(datetime.fromisoformat(start_iso))
    end_dt = tz.localize(datetime.fromisoformat(end_iso))

    event_body = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": timezone_name
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": timezone_name
        }
    }


    event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    return event
