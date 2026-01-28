from datetime import datetime, timedelta
from typing import List
import uuid
from app.util.helper import sanitize_text
from googleapiclient.errors import HttpError

from app.core.config import settings
from app.util.google_credential_manager import GoogleCredentials
from app.util.date_utils import get_day_range


class CalenderService:
    """
    Google Calendar API service layer
    ONLY external API calls
    """

    # ---------------------------------------------------------
    # FETCH BUSY SLOTS
    # ---------------------------------------------------------
    @staticmethod
    def fetch_busy_slots(date: str) -> List[dict]:
        """
        Fetch raw busy slots for a given date
        """
        try:
            service = GoogleCredentials.get_calendar_service()

            start_dt, end_dt = get_day_range(date)

            response = service.freebusy().query(
                body={
                    "timeMin": start_dt.isoformat(),
                    "timeMax": end_dt.isoformat(),
                    "items": [
                        {"id": settings.GOOGLE_CALENDAR_ID}
                    ],
                }
            ).execute()

            return response["calendars"][settings.GOOGLE_CALENDAR_ID]["busy"]

        except HttpError as e:
            print("Google Calendar API Error:", e)
            return []

        except Exception as e:
            print("Unexpected error while fetching busy slots:", e)
            return []

    # ---------------------------------------------------------
    # CHECK SLOT AVAILABILITY
    # ---------------------------------------------------------
    @staticmethod
    def is_slot_available(
        start_datetime: datetime,
        end_datetime: datetime,
        busy_slots: List[dict],
    ) -> bool:
        """
        Check if requested slot overlaps with busy slots
        """
        for busy in busy_slots:
            busy_start = datetime.fromisoformat(busy["start"])
            busy_end = datetime.fromisoformat(busy["end"])

            if start_datetime < busy_end and end_datetime > busy_start:
                return False

        return True

    # ---------------------------------------------------------
    # BOOK MEETING WITH GOOGLE MEET
    # ---------------------------------------------------------
    @staticmethod
    def book_meeting(
        date: str,
        start_time: str,
        duration: int,
        title: str,
        description: str,
        attendees: List[str] | None = None,
    ) -> dict:
        """
        Create Google Calendar event with Google Meet link
        """
        try:
            service = GoogleCredentials.get_calendar_service()

            # Day timezone reference
            start_dt, _ = get_day_range(date)

            start_datetime = datetime.strptime(
                f"{date} {start_time}", "%Y-%m-%d %H:%M"
            ).replace(tzinfo=start_dt.tzinfo)

            end_datetime = start_datetime + timedelta(minutes=duration)

            # -------------------------------
            # Busy slot validation
            # -------------------------------
            busy_slots = CalenderService.fetch_busy_slots(date)

            if not CalenderService.is_slot_available(
                start_datetime, end_datetime, busy_slots
            ):
                return {
                    "status": "error",
                    "message": "Selected slot is already busy",
                }

            # -------------------------------
            # Event payload
            # -------------------------------
            event = {
                "summary": sanitize_text(title),
                "description": sanitize_text(description),
                "start": {
                    "dateTime": start_datetime.isoformat(),
                    "timeZone": settings.TIMEZONE,
                },
                "end": {
                    "dateTime": end_datetime.isoformat(),
                    "timeZone": settings.TIMEZONE,
                },
                # "conferenceData": {
                #     "createRequest": {
                #         "requestId": str(uuid.uuid4()),
                #         "conferenceSolutionKey": {
                #             "type": "hangoutsMeet"
                #         },
                #     }
                # },
                "reminders": {
                    "useDefault": True
                },
            }

            # print(event)


            if attendees:
                event["attendees"] = [
                    {"email": email} for email in attendees
                ]

            # -------------------------------
            # Create event
            # -------------------------------
            created_event = service.events().insert(
                calendarId=settings.GOOGLE_CALENDAR_ID,
                body=event,
                conferenceDataVersion=1,  # 🔥 REQUIRED
            ).execute()

            # print(created_event)

            return {
                "status": "success",
                "event_id": created_event.get("id"),
                # "meet_link": created_event.get("hangoutLink"),
                "calendar_link": created_event.get("htmlLink"),
                "start": created_event["start"]["dateTime"],
                "end": created_event["end"]["dateTime"],
            }

        except HttpError as e:
            return {
                "status": "error",
                "message": f"Google API error: {e}",
            }

        # except Exception as e:
        #     return {
        #         "status": "error",
        #         "message": str(e),
        #     }
