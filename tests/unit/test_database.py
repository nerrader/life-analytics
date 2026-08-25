import sqlite3
from pathlib import Path

import pytest

from life_analytics.logic import database


def test_add_daily_summary_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_daily_summary(
        tmp_path / "test.db",
        {
            "summary_date": "2026-04-08",
            "productivity": 5,
            "mood": 5,
            "stress": 5,
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT summary_date, productivity, mood, stress FROM daily_summaries"
        )
        test_row = cursor.fetchone()

    assert test_row == ("2026-04-08", 5, 5, 5)


def test_add_daily_summary_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_daily_summary(
            tmp_path / "test.db",
            {
                "summary_date": "2026-04-08",
                "productivity": 6,
                "mood": 5,
                "stress": 5,
            },
        )


def test_add_activity_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_activity(
        tmp_path / "test.db",
        {
            "activity_date": "2026-04-08",
            "activity_category": "DEV",
            "activity_description": "unit testing",
            "activity_start": "17:34",
            "activity_end": "20:08",
            "effort": 5,
            "enjoyability": 5,
            "energy_before": 5,
            "energy_after": 5,
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT activity_id, activity_category, activity_description,
                   activity_start, activity_end, effort, enjoyability,
                   energy_before, energy_after
            FROM activities
            """
        )
        test_row = cursor.fetchone()

    assert test_row == (
        1,
        "DEV",
        "unit testing",
        "17:34",
        "20:08",
        5,
        5,
        5,
        5,
    )


def test_add_activity_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_activity(
            tmp_path / "test.db",
            {
                "activity_date": "2026-04-08",
                "activity_category": "DEV",
                "activity_description": "unit testing",
                "activity_start": "99:99",
                "activity_end": "99:99",
                "effort": 0,
                "enjoyability": 0,
                "energy_before": 5,
                "energy_after": 5,
            },
        )


def test_add_sleep_with_valid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    database.add_sleep(
        tmp_path / "test.db",
        {
            "sleep_start_time": "2026-04-08T17:37",
            "sleep_end_time": "2026-04-09T06:56",
            "sleep_quality": 5,
            "sleep_type": "sleep",
        },
    )

    with sqlite3.connect(tmp_path / "test.db") as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT sleep_id, sleep_start_time, sleep_end_time,
                   sleep_quality, sleep_type
            FROM sleep
            """
        )
        test_row = cursor.fetchone()

    assert test_row == (
        1,
        "2026-04-08T17:37",
        "2026-04-09T06:56",
        5,
        "sleep",
    )


def test_add_sleep_with_invalid_data(tmp_path: Path) -> None:
    database.create_database(tmp_path / "test.db")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_sleep(
            tmp_path / "test.db",
            {
                "sleep_start_time": "2026-04-08T17:37",
                "sleep_end_time": "2026-04-09T06:56",
                "sleep_quality": 6,
                "sleep_type": "sleep",
            },
        )
