from datetime import datetime, time


def combine_date_and_time(time: str, date: datetime) -> datetime:
    # change it to a time object
    polished_time: time = datetime.strptime(  # noqa: DTZ007
        time, "%H:%M"
    ).time()

    # so we can use it to replace the hour and minute of the generated yesterdays date
    return date.replace(
        hour=polished_time.hour,
        minute=polished_time.minute,
    )
