from datetime import date, datetime, time

from life_analytics.logic import time_utils


def test_combine_date_and_time_with_valid_inputs() -> None:
    test_datetime = datetime(year=2026, month=12, day=12, hour=19, minute=50)  # noqa: DTZ001
    test_time = time(hour=19, minute=50)
    test_date = date(year=2026, month=12, day=12)

    assert time_utils.combine_date_and_time(test_date, test_time) == test_datetime


def test_combine_date_and_time_with_time_being_string_input() -> None:
    test_time = time(hour=19, minute=50)
    test_date = date(year=2026, month=12, day=12)

    test_time2 = "19:50"
    test_date2 = date(year=2026, month=12, day=12)

    assert time_utils.combine_date_and_time(
        test_date, test_time
    ) == time_utils.combine_date_and_time(test_date2, test_time2)


def test_combine_date_and_time_at_midnight() -> None:
    test_datetime = datetime(year=2026, month=12, day=12)  # noqa: DTZ001
    test_time = time()
    test_date = date(year=2026, month=12, day=12)

    assert time_utils.combine_date_and_time(test_date, test_time) == test_datetime
