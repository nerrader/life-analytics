from datetime import date, datetime
from datetime import time as dt_time


def combine_date_and_time(date: date, time: str | dt_time) -> datetime:
    # change it to a time object
    if isinstance(time, str):
        time_object: dt_time = datetime.strptime(time, "%H:%M").time()
    else:
        time_object = time

    # so we can use it to replace the hour and minute of the generated yesterdays date
    return datetime(  # noqa: DTZ001
        year=date.year,
        month=date.month,
        day=date.day,
        hour=time_object.hour,
        minute=time_object.minute,
    )


def validate_time(time: str | None) -> bool:
    """Validates the time string. Returns True if time is valid, and vice versa."""
    try:
        if time is None:
            return False
        # all it does is just see if this code runs without errors
        datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False


def validate_datetime(date_time: str | None) -> bool:
    """Validates the time string. Returns True if time is valid, and vice versa."""
    try:
        if date_time is None:
            return False
        # all it does is just see if this code runs without errors
        datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def datetime_string_to_iso(date_time: str) -> str:
    try:
        return datetime.strptime(date_time, "%Y-%m-%d %H:%M").isoformat(
            timespec="minutes"
        )
    except ValueError:
        raise ValueError(
            f"Invalid datetime '{date_time}'. Expected format: YYYY-MM-DD HH:MM."
        )
