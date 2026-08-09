from datetime import date, datetime
from datetime import time as dt_time


def combine_date_and_time(date: date, time: str | dt_time) -> datetime:
    # change it to a time object
    if isinstance(time, str):
        time_object: dt_time = datetime.strptime(  # noqa: DTZ007
            time, "%H:%M"
        ).time()
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
