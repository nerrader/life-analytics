from datetime import date, datetime, time

import pytest

from life_analytics.utils import time_utils


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


def test_validate_datetime() -> None:
    assert time_utils.validate_datetime("2026-09-15 18:30") is True
    assert time_utils.validate_datetime("2026-13-15 18:30") is False
    assert time_utils.validate_datetime("2026-09-15 25:30") is False
    assert time_utils.validate_datetime("2026-09-15") is False


def test_datetime_string_to_iso() -> None:
    assert time_utils.datetime_string_to_iso("2026-09-15 8:30") == "2026-09-15T08:30"

    with pytest.raises(ValueError):
        time_utils.datetime_string_to_iso("2026-13-15 18:30")
    with pytest.raises(ValueError):
        time_utils.datetime_string_to_iso("2026-09-15 25:30")
    with pytest.raises(ValueError):
        time_utils.datetime_string_to_iso("2026-09-15")
