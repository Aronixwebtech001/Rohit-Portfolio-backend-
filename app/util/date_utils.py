from datetime import datetime, time
from zoneinfo import ZoneInfo
from app.core.config import settings


def get_day_range(date_str: str):
    """
    Frontend date (YYYY-MM-DD) → timezone aware start & end datetime
    """
    tz = ZoneInfo(settings.TIMEZONE)

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    start_of_day = datetime.combine(date_obj, time.min).replace(tzinfo=tz)
    end_of_day = datetime.combine(date_obj, time.max).replace(tzinfo=tz)

    return start_of_day, end_of_day
