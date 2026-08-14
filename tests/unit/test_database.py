import sqlite3
from pathlib import Path

import pytest

from life_analytics.logic import database


def test_add_daily_summary_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_daily_summary(tmp_path / "test.db", "2026-04-08", 5, 5, 5)

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT summary_date, productivity, mood, stress FROM daily_summaries"
        )
        test_row = cursor.fetchone()

    assert test_row == ("2026-04-08", 5, 5, 5)


def test_add_daily_summary_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    # this is literally supposed to be invalid data for testing
    # which is why we have type: ignore[arg-type]
    with pytest.raises(sqlite3.IntegrityError):
        database.add_daily_summary(tmp_path / "test.db", "2026-20-20", -500, 11, 0)


def test_add_activity_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_activity(
        tmp_path / "test.db",
        "2026-20-20",
        "DEV",
        "unit testing",
        "17:34",
        "20:08",
        5,
        5,
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT activity_id, activity_date, activity_category, activity_description, activity_start, activity_end, effort, enjoyability FROM activities"
        )
        test_row = cursor.fetchone()

    assert test_row == (1, "2026-20-20", "DEV", "unit testing", "17:34", "20:08", 5, 5)


def test_add_activity_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    # this is literally supposed to be invalid data for testing
    # which is why we have type: ignore[arg-type]
    with pytest.raises(sqlite3.IntegrityError):
        database.add_activity(
            database_path=tmp_path / "test.db",
            date="2026-20-20",
            activity_category="DEV",
            activity_description="unit testing",
            activity_start=50,  # type: ignore[arg-type]
            activity_end="99:99",
            effort=0,
            enjoyability=0,
        )


def test_add_sleep_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")
    database.add_sleep(tmp_path / "test.db", "2026-04-08T17:37", "2026-04-09T06:56", 5)

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT sleep_id, sleep_start_time, sleep_end_time, sleep_quality FROM sleep"
        )
        test_row = cursor.fetchone()

    assert test_row == (1, "2026-04-08T17:37", "2026-04-09T06:56", 5)


def test_add_sleep_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    # this is literally supposed to be invalid data for testing
    # which is why we have type: ignore[arg-type]
    with pytest.raises(sqlite3.IntegrityError):
        database.add_sleep(tmp_path / "test.db", "2026-20-01", 5, 11)  # type: ignore[arg-type]
