from datetime import datetime, timedelta
from typing import List
import pytz



def is_overlapping(start, end, busy_slots):
    for slot in busy_slots:
        busy_start = datetime.fromisoformat(slot["start"])
        busy_end = datetime.fromisoformat(slot["end"])

        if start < busy_end and end > busy_start:
            return True
    return False


def round_to_next_hour(dt: datetime) -> datetime:
    if dt.minute == 0 and dt.second == 0:
        return dt
    return (dt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)


def sanitize_text(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("\r", " ")
            .replace("\n", " ")
            .replace("\t", " ")
    )
